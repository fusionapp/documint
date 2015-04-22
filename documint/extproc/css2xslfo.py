import tempfile
from functools import partial
from os.path import expanduser

from twisted.python.filepath import FilePath

from documint.extproc.common import getProcessOutput, which
from documint.extproc.fop import fop
from documint.util import defertee



FOP_CONFIG = FilePath(expanduser('~/.config/documint/fop.xconf'))
findCSS2XSLFO = partial(which, 'css2xslfo')



def css2xslfo(xhtmlPath, xslfoPath):
    """
    Invoke I{CSS2XSLFO}.

    @type  xhtmlPath: L{FilePath}
    @param xhtmlPath: Path to read I{XHTML} input from.

    @type  xslfoPath: L{FilePath}
    @param xslfoPath: Path to write I{XSL-FO} output to.

    @raises ExternalProcessError: If I{CSS2XSLFO} did not exit successfully.

    @rtype: C{Deferred}
    @return: Deferred that fires when the process is complete.
    """
    def checkStatus((out, err, code)):
        return xslfoPath.getsize() > 0

    return getProcessOutput(
        findCSS2XSLFO(),
        ['-fo', xslfoPath.path,
         xhtmlPath.path],
        checkStatus=checkStatus)



def renderXHTML(markup, tempDir=None, css2xslfo=css2xslfo, fop=fop):
    """
    Render an I{XHTML} document to a I{PDF} document.

    @type  markup: L{str}
    @param markup: I{XHTML} document, encoded as UTF-8, that includes
        stylesheet information.

    @rtype: L{Deferred} firing with L{str}
    @return: Deferred that fires with the generated I{PDF} byte data.
    """
    def _removeTemp(ignored):
        tempDir.remove()

    if tempDir is None:
        tempDir = FilePath(tempfile.mkdtemp())
    xhtmlPath = tempDir.child('input.html')
    xhtmlPath.setContent(markup)
    xslfoPath = tempDir.child('output.fo')
    pdfPath = tempDir.child('output.pdf')

    configPath = FOP_CONFIG
    if not configPath.exists():
        configPath = None

    d = css2xslfo(xhtmlPath, xslfoPath)
    d.addCallback(lambda ignored: fop(xslfoPath, pdfPath, configPath))
    d.addCallback(defertee, _removeTemp)
    return d


__all__ = ['css2xslfo', 'renderXHTML']
