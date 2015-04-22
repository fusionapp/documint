from functools import partial

from documint.extproc.common import getProcessOutput, which



findFop = partial(which, 'fop')



def fop(inputFile, outputFile, configFile=None):
    """
    Run Apache FOP.

    @type  inputFile: L{twisted.python.filepath.FilePath}
    @param inputFile: Input file path.

    @type  outputFile: L{twisted.python.filepath.FilePath}
    @param outputFile: Output file path.

    @type  configFile: L{twisted.python.filepath.FilePath}
    @param configFile: Optional config file path.

    @raise L{ExternalProcessError}: If FOP fails to complete successfully.

    @rtype: C{Deferred<str>}
    @return: Deferred that fires with the byte data of the resulting PDF
        document.
    """
    def _readData(ignored):
        return outputFile.getContent()

    args = []
    if configFile is not None:
        args.extend(['-c', configFile.path])
    args.extend([inputFile.path, outputFile.path])
    d = getProcessOutput(findFop(), args)
    d.addCallback(_readData)
    return d
