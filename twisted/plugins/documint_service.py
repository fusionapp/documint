from twisted.application import strports
from twisted.application.service import IServiceMaker
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from twisted.protocols.amp import AMP
from twisted.python import usage
from zope.interface import implementer

from documint.commands import Minter, SimpleMinter



class Options(usage.Options):
    optParameters = [
        ['port', 'p', 'tcp:8750', 'Documint service strport description']]



@implementer(IServiceMaker, IPlugin)
class DocumintServiceMaker(object):
    tapname = 'documint'
    description = 'Document creation service'
    options = Options


    def makeService(self, options):
        factory = Factory()
        factory.protocol = lambda: AMP(
            locator=Minter(signPDF=self._signPDF(options)))
        return strports.service(options['port'], factory, reactor=reactor)


serviceMaker = DocumintServiceMaker()
