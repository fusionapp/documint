"""
I{Documint} utility functions.
"""
from StringIO import StringIO

from lxml import etree
from twisted.internet.defer import maybeDeferred



def embedStylesheets(markup, stylesheets, removeStylesheets=False):
    """
    Embed external stylesheets in I{XHTML} markup.

    @type  markup: L{str}
    @param markup: I{XHTML} markup UTF-8 byte data.

    @type  stylesheets: I{iterable} of L{str}
    @param stylesheets: Iterable of stylesheet UTF-8 byte data to embed.

    @rtype: L{str}
    @return: I{XHTML} UTF-8 byte data with embedded stylesheets.
    """
    tree = etree.parse(StringIO(markup))
    namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
    head = tree.xpath('//xhtml:head', namespaces=namespaces)[0]

    for stylesheet in stylesheets:
        e = etree.SubElement(
            head,
            '{http://www.w3.org/1999/xhtml}style',
            attrib=dict(type='text/css'))
        e.text = stylesheet.decode('utf-8')

    if removeStylesheets:
        stylesheetLinks = head.xpath(
            'xhtml:link[@rel="stylesheet"]', namespaces=namespaces)
        for e in stylesheetLinks:
            head.remove(e)

    return etree.tostring(tree, encoding='utf-8')


def defertee(result, func, *a, **kw):
    """
    Call C{func}, with positional and keyword arguments, as a side effect, and
    return C{result}.

    Useful in combination with C{Deferred.addCallback} when you wish to perform
    an operation in the callback chain but wish to retain the result for
    subsequent callbacks.
    """
    d = maybeDeferred(func, result, *a, **kw)
    d.addCallback(lambda ignored: result)
    return d



__all__ = ['embedStylesheets']
