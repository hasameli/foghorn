#!/usr/bin/env python

""" The foghorn daemon """

import logging
import socket
from twisted.internet import reactor
from twisted.names import client, dns, server
from twisted.internet.address import IPv4Address

from FoghornSettings import FoghornSettings
from Foghorn import Foghorn


class FoghornDNSServerFactory(server.DNSServerFactory):
    """ Create DNS Servers """
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
    """ Load settings and start the server """
    foghorn = None
    settings = None

    def __init__(self):
        self.settings = FoghornSettings()
        self.foghorn = Foghorn(self.settings)
        self.init_logging()

    def init_logging(self):
        """ Initalize logging objects """
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
        """ Kick off the server """
        factory = FoghornDNSServerFactory(
            clients=[self.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
        )
        protocol = dns.DNSDatagramProtocol(controller=factory)

        reactor.listenUDP(self.settings.DNSPort, protocol)
        reactor.listenTCP(self.settings.DNSPort, factory)

        reactor.run()
        self.foghorn.save_state()

if __name__ == '__main__':
    FOGHORN = Main()
    FOGHORN.run()
