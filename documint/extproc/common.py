from os.path import exists
from warnings import warn

from twisted.internet.utils import getProcessOutputAndValue
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.python.procutils import which as twisted_which

from documint.errors import ExternalProcessError, NoSuchFile
from documint.util import defertee



def _checkStatus((out, err, code)):
    """
    Check that the exit status is C{0}.
    """
    return code == 0



def getProcessOutput(binary, args,
                     getProcessOutputAndValue=getProcessOutputAndValue,
                     checkStatus=_checkStatus):
    """
    Spawn a new process and return the standard output.

    @type  binary: C{str}
    @param binary: Path to the binary to spawn.

    @type  args: C{sequence} of C{str}
    @param args: Arguments to pass when spawning L{binary}.

    @param getProcessOutputAndValue: Callable to spawn a process and return
        C{(standard output, standard error, exit status)}. Defaults to
        L{twisted.internet.utils.getProcessOutputAndValue}

    @raise L{ExternalProcessError}: If the exit status is non-zero.

    @rtype: C{Deferred<str>}
    @return: Deferred firing with the standard output of L{binary}.
    """
    def _log((out, err, code)):
        name = FilePath(binary).basename()
        log.msg('%s command: %r' % (name, (binary, args)))

    def _check((out, err, code)):
        if not checkStatus((out, err, code)):
            raise ExternalProcessError(binary, args, code, (out, err))
        return out

    d = getProcessOutputAndValue(binary, args)
    d.addCallback(defertee, _log)
    d.addCallback(_check)
    return d



def sanitizePaths(paths):
    """
    Convert an iterable of C{FilePath}s to an iterable of C{str}.
    """
    for path in paths:
        if isinstance(path, (str, unicode)):
            warn(
                'paths should be twisted.python.filepath.FilePath not %r' % (
                    type(path),),
                DeprecationWarning, 2)
            path = FilePath(path)

        fn = path.path
        if isinstance(fn, unicode):
            fn = fn.encode('ascii')

        if not exists(fn):
            raise NoSuchFile(fn)

        yield fn



def which(binary, _which=twisted_which):
    """
    Locate the first binary in the path.

    @type  binary: C{str}
    @param binary: Name of the binary to find.

    @param _which: Callable taking one parameter, the name of the binary to
        find, returning a list of possibilities.

    @raise RuntimeError: If the binary could not be located.

    @return: Path of the binary.
    """
    paths = _which(binary)
    if paths:
        return paths[0]
    raise RuntimeError('binary %r not found' % (binary,))
