"""
I{Documint} I{AMP} client.
"""
from twisted.internet import task
from twisted.internet.endpoints import clientFromString, connectProtocol
from twisted.protocols.amp import AMP

from documint.commands import Render



def render(protocol, markup, stylesheets):
    """
    Execute the L{Render} command on an AMP protocol instance.
    """
    return protocol.callRemote(
        Render,
        markup=markup,
        stylesheets=stylesheets)



__all__ = ['render']



if __name__ == '__main__':
    import sys
    def main(reactor, markup, styles):
        def _readFile(name):
            with file(name, 'rb') as fd:
                return fd.read()

        def _writeResponse(response):
            sys.stdout.write(response['data'])
            sys.stdout.flush()

        endpoint = clientFromString(reactor, 'tcp:host=127.0.0.1:port=8750')
        d = connectProtocol(endpoint, AMP())
        d.addCallback(render, _readFile(markup), map(_readFile, styles))
        d.addCallback(_writeResponse)
        return d

    task.react(main, (sys.argv[1], sys.argv[2:]))
