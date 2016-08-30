# You can run this .tac file directly with:
#    twistd -ny service.tac

"""
This .tac file starts the foghorn DNS proxying daemon
according to the settings in foghornd/settings.json
"""

from twisted.application import service, internet
from twisted.names import client, dns

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

    factory = FoghornDNSServerFactory(
        clients=[foghorn.foghorn, client.Resolver(resolv='/etc/resolv.conf')]
    )

    udp_protocol = dns.DNSDatagramProtocol(controller=factory)
    udp_server = internet.UDPServer(foghorn.settings.dns_port, udp_protocol)
    tcp_server = internet.TCPServer(foghorn.settings.dns_port, factory)
    xml_server = internet.TCPServer(7080, webserver.Site(foghorn.foghornrpc))
    return [udp_server, tcp_server, xml_server]


# This is the required part of the .tac file to start
# the service as a daemon
application = service.Application("foghorn")

# attach the service to its parent application
for item in foghord_service():
    item.setServiceParent(application)
