# You can run this .tac file directly with:
#    twistd -ny service.tac

"""
This .tac file starts the foghorn DNS proxying daemon
according to the settings in foghornd/settings.json
"""

import netifaces
from twisted.application import service, internet
from twisted.names import dns, cache

from twisted.web import server as webserver

from foghornd import Foghorn, FoghornSettings
from foghornd.foghornrpc import FoghornXMLRPC
from foghornd.foghorndnsserverfactory import FoghornDNSServerFactory


class Main(object):
    """Load settings and start the server"""

    foghorn = None
    settings = None

    def __init__(self):
        self.settings = FoghornSettings()
        self.foghorn = Foghorn(self.settings)
        self.foghornrpc = FoghornXMLRPC()
        self.foghornrpc.foghorn = self.foghorn
        self.foghornrpc.allowNone = 1


def foghord_service():
    """Return a service suitable for creating an application object."""
    # create a resource to serve static files
    foghorn = Main()
    servers = []

    factory = FoghornDNSServerFactory(
        caches=[cache.CacheResolver()],
        clients=[foghorn.foghorn]
    )
    factory.noisy = False

    addresses = []
    try:
        addresses = foghorn.settings.listen
    except AttributeError:
        pass

    if not addresses:
        for iface in netifaces.interfaces():
            for addr in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
                addresses.append(addr["addr"])

    for listen in addresses:
        udp_protocol = dns.DNSDatagramProtocol(controller=factory)
        udp_protocol.noisy = False
        udp_server = internet.UDPServer(foghorn.settings.dns_port, udp_protocol, interface=listen)
        udp_server.noisy = False
        servers.append(udp_server)

        tcp_server = internet.TCPServer(foghorn.settings.dns_port, factory, interface=listen)
        servers.append(tcp_server)

    #xml_server = internet.TCPServer(7080, webserver.Site(foghorn.foghornrpc))
    rpcsite = webserver.Site(foghorn.foghornrpc)
    rpcsite.noisy = False
    xml_server = internet.UNIXServer("foghornd.sock", rpcsite)
    servers.append(xml_server)

    return servers


# This is the required part of the .tac file to start
# the service as a daemon
application = service.Application("foghorn")

# attach the service to its parent application
for item in foghord_service():
    item.setServiceParent(application)
