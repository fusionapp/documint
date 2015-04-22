"""
Tests for L{documint.util}.
"""
from StringIO import StringIO

from lxml import etree
from twisted.trial.unittest import TestCase

from documint.util import embedStylesheets



class EmbedStylesheetsTests(TestCase):
    """
    Tests for L{documint.util.embedStylesheets}.
    """
    def test_removeStylesheetLinks(self):
        """
        L{documint.util.embedStylesheets} removes links with the
        C{'stylesheet'} relationship.
        """
        markup = embedStylesheets('''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head>
    <link href="test.css" type="text/css" rel="stylesheet" />
    <link type="text/css" rel="something" />
</head><body></body></html>''', [], removeStylesheets=True)
        tree = etree.parse(StringIO(markup))
        namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
        elems = tree.findall('//xhtml:head/xhtml:link', namespaces=namespaces)
        self.assertEquals(1, len(elems))
        self.assertEquals('something', elems[0].get('rel'))


    def test_embedStylesheets(self):
        """
        L{documint.util.embedStylesheets} embeds stylesheets in I{style}
        elements.
        """
        stylesheets = [
            'div {color:red;}',
            'span {color:blue;}']
        markup = embedStylesheets('''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><head></head><body></body></html>''', stylesheets)
        tree = etree.parse(StringIO(markup))
        namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
        elems = tree.findall('//xhtml:head/xhtml:style', namespaces=namespaces)
        self.assertEquals(2, len(elems))
        for elem, stylesheet in zip(elems, stylesheets):
            self.assertEquals(stylesheet, elem.text)
