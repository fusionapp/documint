"""
Tests for L{documint.commands}.
"""
from twisted.internet.defer import succeed
from twisted.trial.unittest import TestCase

from documint.commands import Minter, SimpleMinter



class MinterTests(TestCase):
    """
    Tests for L{documint.commands.Minter}.
    """
    def test_render(self):
        """
        L{Minter.render}, a responder for L{documint.commands.Render}, invokes
        L{Minter.renderXHTML}.
        """
        minter = Minter()
        minter.renderXHTML = lambda *a: succeed((a, 'application/pdf'))
        d = minter.render('markup', ['css1', 'css2'])
        d.addCallback(
            self.assertEquals,
            {'data': ('markup', ['css1', 'css2']),
             'contentType': 'application/pdf'})
        return d



class SimpleMinterTests(TestCase):
    """
    Tests for L{documint.commands.SimpleMinter}.
    """
    def test_renderXHTML(self):
        """
        L{SimpleMinter.renderXHTML} invokes L{Minter.embedStylesheets}.
        """
        minter = SimpleMinter()
        minter.embedStylesheets = lambda *a: a
        d = minter.renderXHTML('markup', ['css1', 'css2'])
        d.addCallback(
            self.assertEquals, (('markup', ['css1', 'css2']), 'text/html'))
        return d
