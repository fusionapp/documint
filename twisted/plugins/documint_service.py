from twisted.application import strports
from twisted.application.service import IServiceMaker
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements

from documint.commands import Minter, SimpleMinter



class Options(usage.Options):
    optFlags = [
        ['simple', 's', 'Simple Documint service']]

    optParameters = [
        ['port', 'p', 'tcp:8750', 'Documint service strport description']]



class DocumintServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'documint'
    description = 'Document creation service'
    options = Options


    def makeService(self, options):
        factory = Factory()
        if options['simple']:
            factory.protocol = SimpleMinter
        else:
            factory.protocol = Minter
        return strports.service(options['port'], factory, reactor=reactor)


serviceMaker = DocumintServiceMaker()
