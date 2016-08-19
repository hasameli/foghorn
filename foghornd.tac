# You can run this .tac file directly with:
#    twistd -ny service.tac

"""
This .tac file starts the foghorn DNS proxying daemon
according to the settings in foghornd/settings.json
"""

import logging
import socket
from twisted.application import service, internet
from twisted.internet import reactor
from twisted.names import client, dns, server
from twisted.internet.address import IPv4Address

from foghornd import Foghorn, FoghornSettings


class FoghornDNSServerFactory(server.DNSServerFactory):
    """Create DNS Servers"""

    logger = logging.getLogger('foghornd')
    peer_address = ""

    def handleQuery(self, message, protocol, address):
        """Override handleQuery so we get the request address"""
        if protocol.transport.socket.type == socket.SOCK_STREAM:
            self.peer_address = protocol.transport.getPeer()
        elif protocol.transport.socket.type == socket.SOCK_DGRAM:
            self.peer_address = IPv4Address('UDP', *address)
        else:
            self.logger.warn("Unexpected socket type %r", protocol.transport.socket.type)

        # Make peer_address available to resolvers that support that attribute
        for resolver in self.resolver.resolvers:
            if hasattr(resolver, 'peer_address'):
                resolver.peer_address = self.peer_address

        return server.DNSServerFactory.handleQuery(self, message, protocol, address)

class Main(object):
    """Load settings and start the server"""

    foghorn = None
    settings = None

    def __init__(self):
        self.settings = FoghornSettings()
        self.foghorn = Foghorn(self.settings)
        self.init_logging()

    def init_logging(self):
        """Initalize logging objects"""
        logger = logging.getLogger('foghornd')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s")
        log_streamhandler = logging.StreamHandler()
        log_streamhandler.setLevel(logging.DEBUG)
        log_streamhandler.setFormatter(formatter)
        logger.addHandler(log_streamhandler)
        file_handle = logging.FileHandler(self.settings.logfile)
        file_handle.setLevel(logging.DEBUG)
        file_handle.setFormatter(formatter)
        logger.addHandler(file_handle)

    def run(self):
        """Kick off the server"""
        factory = FoghornDNSServerFactory(
            clients=[self.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
        )
        protocol = dns.DNSDatagramProtocol(controller=factory)

        # Pylint can't seem to find these methods.
        # pylint: disable=E1101
        reactor.listenUDP(self.settings.dns_port, protocol)
        reactor.listenTCP(self.settings.dns_port, factory)
        reactor.run()
        self.foghorn.save_state()


def foghord_service():
    """Return a service suitable for creating an application object."""
    # create a resource to serve static files
    foghorn = Main()

    factory = FoghornDNSServerFactory(
        clients=[foghorn.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    return internet.UDPServer(foghorn.settings.dns_port, protocol)


if __name__ == '__main__':
    FOGHORN = Main()
    FOGHORN.run()
else:
    # This is the required part of the .tac file to start
    # the service as a daemon
    application = service.Application("foghorn")

    # attach the service to its parent application
    service = foghord_service()

    service.setServiceParent(application)
