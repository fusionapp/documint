# From lp:~glyph/+junk/amphacks
"""
An argument type for sending medium-sized strings (more than 64k, but small
enough that they still fit into memory and don't require streaming).
"""

from cStringIO import StringIO
from itertools import count

from twisted.protocols.amp import AMP, Argument, Command



CHUNK_MAX = 0xffff

class BigString(Argument):
    def fromBox(self, name, strings, objects, proto):
        value = StringIO()
        value.write(strings.get(name))
        for counter in count(2):
            chunk = strings.get("%s.%d" % (name, counter))
            if chunk is None:
                break
            value.write(chunk)
        objects[name] = value.getvalue()


    def toBox(self, name, strings, objects, proto):
        value = StringIO(objects[name])
        firstChunk = value.read(CHUNK_MAX)
        strings[name] = firstChunk
        counter = 2
        while True:
            nextChunk = value.read(CHUNK_MAX)
            if not nextChunk:
                break
            strings["%s.%d" % (name, counter)] = nextChunk
            counter += 1

class Send(Command):
    arguments = [('big', BigString())]

class Example(AMP):
    @Send.responder
    def gotBig(self, big):
        print 'Got a big input', len(big)
        f = file("OUTPUT", "wb")
        f.write(big)
        f.close()
        return {}

def main(argv):
    from twisted.internet import reactor
    from twisted.internet.protocol import Factory, ClientCreator
    if argv[1] == 'client':
        filename = argv[2]
        def connected(result):
            result.callRemote(Send, big=file(filename).read())
        ClientCreator(reactor, AMP).connectTCP("localhost", 4321).addCallback(
            connected)
        reactor.run()
    elif argv[1] == 'server':
        f = Factory()
        f.protocol = Example
        reactor.listenTCP(4321, f)
        reactor.run()
    else:
        print "Specify 'client' or 'server'."
if __name__ == '__main__':
    from sys import argv as arguments
    main(arguments)
