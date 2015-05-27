"""
Documint I{AMP} command and protocol definitions.
"""
from lxml import etree
from twisted.internet.defer import succeed
from twisted.protocols import amp
from twisted.python.failure import Failure

from documint.errors import (
    ExternalProcessError, RemoteExternalProcessError, UnsupportedContentType,
    XMLSyntaxError)
from documint.extproc.css2xslfo import renderXHTML
from documint.extproc.neon import failingPDFSign
from documint.mediumbox import BigString
from documint.util import embedStylesheets



class Render(amp.Command):
    """
    Render I{XHTML} markup and I{CSS} documents to a I{PDF} document.

    Accepts the following arguments:

    * C{markup}, a L{str}, that is the I{XHTML} markup byte data;
    * C{stylesheets}, a L{list} of L{str}, that is a list of stylesheet byte
      data.

    Returns a L{dict} mapping C{'data'} to a C{str} of rendered byte data, and
    C{'contentType'} to the content type of the byte data.
    """
    arguments = [
        ('markup', BigString()),
        ('stylesheets', amp.ListOf(amp.String()))]

    response = [
        ('data', BigString()),
        ('contentType', amp.String())]

    errors = {
        XMLSyntaxError: 'XML_SYNTAX_ERROR',
        RemoteExternalProcessError: 'EXTERNAL_PROCESS_ERROR'}



class Certify(amp.Command):
    """
    Sign a I{PDF} document with the configured keystore.
    """
    arguments = [
        ('data', BigString()),
        ('contentType', amp.String()),
        ('reason', amp.String()),
        ('location', amp.String())]

    response = [
        ('data', BigString()),
        ('contentType', amp.String())]

    errors = {
        UnsupportedContentType: 'UNSUPPORTED_CONTENT_TYPE',
        RemoteExternalProcessError: 'EXTERNAL_PROCESS_ERROR'}



class Minter(amp.CommandLocator):
    """
    Documint command locator.

    This implementation is for performing the full range of tasks that produce
    PDF documents.
    """
    def __init__(self, signPDF=failingPDFSign):
        """
        @param signPDF: Something like L{documint.extproc.neon.signPDF} with the
            keystore, keystore password and private key parameters already
            partially applied.
        """
        self._signPDF = signPDF


    def embedStylesheets(self, markup, stylesheets):
        """
        Embed external stylesheets in I{XHTML} markup.

        @type  markup: L{str}
        @param markup: I{XHTML} markup byte data.

        @type  stylesheets: I{iterable} of L{str}
        @param stylesheets: Iterable of stylesheet byte data to embed.

        @rtype: L{str}
        @return: I{XHTML} markup with embedded stylesheets.
        """
        try:
            return embedStylesheets(markup, stylesheets)
        except etree.XMLSyntaxError, e:
            raise XMLSyntaxError(e)


    def _handleExternalProcessError(self, f):
        """
        Convert L{ExternalProcessError} into L{RemoteExternalProcessError}.
        """
        f.trap(ExternalProcessError)
        return Failure(RemoteExternalProcessError(f.getErrorMessage()))


    def _dataResult(self, (data, contentType)):
        """
        Convert a 2-tuple of data and content type into a dict.
        """
        return dict(data=data,
                    contentType=contentType)


    def _renderXHTML(self, markup, stylesheets):
        """
        Render I{XHMTL} markup and I{CSS} to a I{PDF}.

        @type  markup: L{str}
        @param markup: I{XHTML} UTF-8 byte data.

        @type  stylesheets: I{iterable} of L{str}
        @param stylesheets: Iterable of stylesheet UTF-8 byte data to embed.

        @rtype: L{Deferred} firing with C{(str, str)}
        @return: Deferred that fires with the generated I{PDF} byte data and
            content type.
        """
        d = renderXHTML(self.embedStylesheets(markup, stylesheets))
        d.addErrback(self._handleExternalProcessError)
        d.addCallback(lambda data: (data, 'application/pdf'))
        return d


    @Render.responder
    def render(self, markup, stylesheets):
        d = self._renderXHTML(markup, stylesheets)
        d.addCallback(self._dataResult)
        return d


    def _certifyDocument(self, data, contentType, reason, location):
        """
        Sign a I{PDF} document.
        """
        if contentType != 'application/pdf':
            raise UnsupportedContentType(
                'Only PDF content can be certified, got: {!r}'.format(contentType))
        d = self._signPDF(data=data,
                          reason=reason,
                          location=location)
        d.addErrback(self._handleExternalProcessError)
        d.addCallback(lambda data: (data, 'application/pdf'))
        return d


    @Certify.responder
    def certify(self, data, contentType, reason, location):
        d = self._certifyDocument(data, contentType, reason, location)
        d.addCallback(self._dataResult)
        return d



class SimpleMinter(Minter):
    """
    Documint command locator.

    The main difference between L{SimpleMinter} and L{Minter} is that
    L{SimpleMinter} will output I{XHTML}.
    """
    def _renderXHTML(self, markup, stylesheets):
        """
        Embed I{CSS} in I{XHMTL} markup

        @type  markup: L{str}
        @param markup: I{XHTML} UTF-8 byte data.

        @type  stylesheets: I{iterable} of L{str}
        @param stylesheets: Iterable of stylesheet UTF-8 byte data to embed.

        @rtype: L{Deferred} firing with C{(str, str)}
        @return: Deferred that fires with the generated I{XHTML}, including
            embedded I{CSS} byte data, and the content type.
        """
        return succeed(
            (self.embedStylesheets(markup, stylesheets), 'text/html'))



__all__ = ['Render', 'Minter', 'SimpleMinter', 'Certify']
