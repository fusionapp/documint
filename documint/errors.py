"""
I{Documint} error types.
"""



class XMLSyntaxError(Exception):
    """
    Wrapper around L{lxml.etree.XMLSyntaxError} that requires no additional
    arguments.
    """


class ExternalProcessError(RuntimeError):
    """
    An external process returned an exit status indicating failure.

    @type binary: C{str}
    @ivar binary: Path to the binary to spawn.

    @type arguments: C{sequence} of C{str}
    @ivar arguments: Arguments to pass when spawning L{binary}.

    @type code: C{int}
    @ivar code: Exit status.

    @type stdout: C{str}
    @ivar stdout: Standard output data.

    @type stderr: C{str}
    @ivar stderr: Standard error data.
    """
    def __init__(self, binary, arguments, code, (stdout, stderr)):
        RuntimeError.__init__(self, (binary, arguments, code, (stdout, stderr)))
        self.binary = binary
        self.arguments = arguments
        self.code = code
        self.stdout = stdout
        self.stderr = stderr



class RemoteExternalProcessError(Exception):
    """
    AMP-friendly description of an external process error.
    """



class NoSuchFile(IOError):
    """
    The specified file could not be found.
    """
