#!/usr/bin/env python

import sys, os, logging, time
from datetime import datetime
from twisted.internet import reactor
from twisted.names import client, dns, server
import socket
from twisted.internet.address import IPv4Address

from FoghornSettings import FoghornSettings
from Foghorn import Foghorn

class FoghornDNSServerFactory(server.DNSServerFactory):
  logger = logging.getLogger('foghornd')

  """Override handleQuery so we get the request address"""
  def handleQuery(self, message, protocol, address):
    if protocol.transport.socket.type == socket.SOCK_STREAM:
      self.peer_address = protocol.transport.getPeer()
    elif protocol.transport.socket.type == socket.SOCK_DGRAM:
      self.peer_address = IPv4Address('UDP', *address)
    else:
      logger.warn("Unexpected socket type %r" % protocol.transport.socket.type)

    # Make peer_address available to resolvers that support that attribute
    for resolver in self.resolver.resolvers:
      if hasattr(resolver, 'peer_address'):
        resolver.peer_address = self.peer_address

    return server.DNSServerFactory.handleQuery(self, message, protocol, address)

class Main(object):
  foghorn = None
  settings = None

  def __init__(self):
    self.settings = FoghornSettings()
    self.foghorn = Foghorn(self.settings)
    logger = logging.getLogger('foghornd')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s")
    cl = logging.StreamHandler()
    cl.setLevel(logging.DEBUG)
    cl.setFormatter(formatter)
    logger.addHandler(cl)
    fh = logging.FileHandler(self.settings.logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

  def run(self):
    #kick off the server
    factory = FoghornDNSServerFactory(
        clients=[self.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
    )
    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(self.settings.DNSPort, protocol)
    reactor.listenTCP(self.settings.DNSPort, factory)

    reactor.run()
    self.foghorn.saveState()


if __name__=='__main__':
  foghornd = Main()
  foghornd.run()
