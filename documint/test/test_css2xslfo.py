from twisted.internet.defer import fail, succeed
from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase

from documint.errors import ExternalProcessError
from documint.extproc.css2xslfo import css2xslfo, findCSS2XSLFO, renderXHTML



class CSS2XSLFOTests(TestCase):
    """
    Tests for L{documint.util.css2xslfo}.
    """
    try:
        findCSS2XSLFO()
    except RuntimeError:
        skip = 'css2xslfo unavailable'


    def setUp(self):
        self.dataPath = FilePath(__file__).sibling('data')


    def test_missing(self):
        """
        Invoking I{css2xslfo} with a missing input raises an
        L{ExternalProcessError}.
        """
        def checkException(e):
            self.assertIn('(No such file or directory)', e.stderr)

        outputPath = FilePath(self.mktemp())
        outputPath.touch()
        d = css2xslfo(self.dataPath.child('missing.html'), outputPath)
        d = self.assertFailure(d, ExternalProcessError)
        d.addCallback(checkException)
        return d


    def test_broken(self):
        """
        Invoking I{css2xslfo} with a broken input raises an
        L{ExternalProcessError}.
        """
        def checkException(e):
            self.assertIn(
                'element type "div" must be terminated by the matching end-tag',
                e.stderr)
        outputPath = FilePath(self.mktemp())
        outputPath.touch()
        d = css2xslfo(self.dataPath.child('broken.html'), outputPath)
        d = self.assertFailure(d, ExternalProcessError)
        d.addCallback(checkException)
        return d



class RenderXHMTLTests(TestCase):
    """
    Tests for L{documint.util.renderXHTML}.
    """
    def mkdtemp(self):
        """
        Create a temporary directory.

        @rtype: L{FilePath}
        """
        tempDir = FilePath(self.mktemp())
        if not tempDir.exists():
            tempDir.makedirs()
        return tempDir


    def test_renderXHTML(self):
        """
        L{renderXHTML} invokes L{css2xslfo} then L{fop}, removes the temporary
        directory, and returns I{fop}'s result.
        """
        def mockCSS2XSLFO(xhtmlPath, xslfoPath):
            return succeed(None)

        def mockFop(xslfoPath, pdfPath, configFile=None):
            return succeed('pdf')

        def cb(pdfData):
            self.assertIdentical(str, type(pdfData))
            self.assertEquals('pdf', pdfData)
            self.assertFalse(tempDir.exists())

        tempDir = self.mkdtemp()
        d = renderXHTML(
            'markup',
            tempDir=tempDir,
            css2xslfo=mockCSS2XSLFO,
            fop=mockFop)
        d.addCallback(cb)
        return d


    def test_renderXHTMLCSS2XSLFOFails(self):
        """
        If L{renderXHTML} fails invoking L{css2xslfo}, L{fop} is not invoked
        and the temporary directory is not removed.
        """
        def mockCSS2XSLFO(xslfoPath, xhtmlPath):
            return fail(RuntimeError(1))

        def mockFop(xslfoPath, pdfPath, configFile=None):
            self.fail('Never get here')

        def cb(e):
            self.assertEquals('1', str(e))
            self.assertTrue(tempDir.exists())

        tempDir = self.mkdtemp()
        d = renderXHTML(
            'markup',
            tempDir=tempDir,
            css2xslfo=mockCSS2XSLFO,
            fop=mockFop)
        d = self.assertFailure(d, RuntimeError)
        d.addCallback(cb)
        return d


    def test_renderXHTMLFopFails(self):
        """
        If L{renderXHTML} fails invoking L{fop}, the temporary
        directory is not removed.
        """
        def mockCSS2XSLFO(xhtmlPath, xslfoPath):
            return succeed(None)

        def mockFop(xslfoPath, pdfPath, configFile=None):
            return fail(RuntimeError(2))

        def cb(e):
            self.assertEquals('2', str(e))
            self.assertTrue(tempDir.exists())

        tempDir = self.mkdtemp()
        d = renderXHTML(
            'markup',
            tempDir=tempDir,
            css2xslfo=mockCSS2XSLFO,
            fop=mockFop)
        self.assertFailure(d, RuntimeError)
        d.addCallback(cb)
        return d
