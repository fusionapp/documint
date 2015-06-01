from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase

from documint.errors import ExternalProcessError
from documint.extproc.neon import _neonBinary, signPDF



class NeonTests(TestCase):
    """
    Tests for L{documint.extproc.neon}.
    """
    try:
        _neonBinary()
    except RuntimeError:
        skip = 'clj-neon unavailable.'


    def setUp(self):
        self.keystore = FilePath(
            __file__).sibling('data').child('keystore.jks')
        self.keystorePassword = u'tQ4i4RJKyX6J4Lq1'
        self.privateKeyPassword = u'tQ4i4RJKyX6J4Lq1'


    def signPDF(self, unsignedPDF):
        return signPDF(
            data=unsignedPDF,
            keystorePath=self.keystore,
            keystorePassword=self.keystorePassword,
            reason='Test reason',
            location='Test location',
            privateKeyPassword=self.privateKeyPassword)


    def assertValidPDF(self, data):
        """
        Assert that C{data} is valid PDF data.
        """
        self.assertNotEqual(len(data), 0)
        self.assertTrue(data.startswith('%PDF-'))


    def test_success(self):
        """
        Neon generates a valid document when invoked with valid data.
        """
        unsignedPDF = FilePath(__file__).sibling('data').child('test.pdf')
        d = self.signPDF(unsignedPDF.getContent())
        d.addCallback(self.assertValidPDF)
        return d


    def test_failure(self):
        """
        Invoking Neon with invalid data raises
        L{documint.error.ExternalProcessError}.
        """
        d = self.signPDF('garbage')
        return self.assertFailure(d, ExternalProcessError)
