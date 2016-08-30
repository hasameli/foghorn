"""Create DNS Servers"""

import logging
import socket

from twisted.internet.address import IPv4Address
from twisted.names import server


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
