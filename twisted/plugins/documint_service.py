from functools import partial

from twisted.application import strports
from twisted.application.service import IServiceMaker
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from twisted.protocols.amp import AMP
from twisted.python import usage
from zope.interface import implementer

from documint.commands import Minter
from documint.extproc.neon import signPDF, failingPDFSign



class Options(usage.Options):
    optParameters = [
        ['port', 'p', 'tcp:8750', 'Documint service strport description'],
        ['keystore', None, None, 'Java keystore path'],
        ['password', None, None, 'Keystore password'],
        ['privateKeyPassword', None, None,
         'Password for the private key in the keystore']]



@implementer(IServiceMaker, IPlugin)
class DocumintServiceMaker(object):
    tapname = 'documint'
    description = 'Document creation service'
    options = Options


    def _signPDF(self, options):
        """
        L{documint.extproc.neon.signPDF} with keystore, keystore password and
        private key password partially applied.
        """
        keystorePath = options['keystore']
        if keystorePath is None:
            return failingPDFSign
        keystorePassword = options['password']
        if keystorePassword is None:
            return failingPDFSign
        privateKeyPassword = options['privateKeyPassword']
        return partial(
            signPDF,
            keystorePath=keystorePath,
            keystorePassword=keystorePassword,
            privateKeyPassword=privateKeyPassword)


    def makeService(self, options):
        factory = Factory()
        factory.protocol = lambda: AMP(
            locator=Minter(signPDF=self._signPDF(options)))
        return strports.service(options['port'], factory, reactor=reactor)


serviceMaker = DocumintServiceMaker()
