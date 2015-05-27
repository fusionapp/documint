from functools import partial
from tempfile import mkstemp

from twisted.python.filepath import FilePath

from documint.errors import RemoteExternalProcessError
from documint.extproc.common import getProcessOutput, sanitizePaths, which



_neonBinary = partial(which, 'clj-neon')



def failingPDFSign(*a, **kw):
    """
    Fail to sign anything.
    """
    raise RemoteExternalProcessError('PDF signing is not correctly configured')



def signPDF(data, keystorePath, keystorePassword, reason, location,
            signaturePage=None, fields=None, privateKeyPassword=None,
            imagePath=None, rectangle=None):
    """
    Digitally sign a PDF.

    @param data: Unsigned PDF bytes.
    @type  data: L{str}

    @param keystorePath: The path to the Java Keystore.
    @type  keystorePath: L{twisted.python.filepath.FilePath}

    @param keystorePassword: The Java Keystore password.
    @type  keystorePassword: L{str}

    @param reason: The reason for signing the PDF.
    @type  reason: L{str}

    @param location: The location the PDF was signed.
    @type  location: L{str}

    @param signaturePage: Path to signature page.
    @type  signaturePage: L{FilePath} or L{None}

    @param fields: Mapping of signature page field names and values.
    @type  fields: L{dict}

    @param privateKeyPassword: The password for the private key contained in
        the Java Keystore.
    @type  privateKeyPassword: L{str} or L{None}

    @param imagePath: The path to an image to stamp on the PDF.
    @type  imagePath: L{twisted.python.filepath.FilePath}

    @param rectangle: The size of the signature rectangle. eg:
        [LX1,LY1,UX2,UY2]
    @type  rectangle: L{list} of L{str}

    @return: A deferred resulting in the signed PDF content as a byte string or
        a L{diamond.error.ExternalProcessError}.
    """
    tempPath = FilePath(mkstemp()[1])
    tempPath.setContent(data)

    def _cleanup(result):
        tempPath.remove()
        return result

    keystorePath, inputPath = sanitizePaths([keystorePath, tempPath])
    args = [inputPath,
            '-',
            keystorePath,
            '--keystore-pass', keystorePassword,
            '--reason', reason,
            '--location', location]

    if privateKeyPassword:
        args.extend(['--password', privateKeyPassword])
    if imagePath:
        args.extend(['--signature-image', imagePath])
    if rectangle:
        args.extend(['--signature-rect', ','.join(rectangle)])
    if signaturePage:
        args.extend(['--signature-page', signaturePage.path])
    if fields:
        for k, v in fields.iteritems():
            args.extend(['--field', '%s:%s' % (k, v)])
    d = getProcessOutput(_neonBinary(), args)
    d.addBoth(_cleanup)
    return d
