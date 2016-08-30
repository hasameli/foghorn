"""XMLRPC API"""

from twisted.web import xmlrpc


class FoghornXMLRPC(xmlrpc.XMLRPC):
    """
    Foghorn API via XMLRPC
    """

    foghorn = {}

    def xmlrpc_toggle_baseline(self):
        """Toggle baseline"""
        self.foghorn.toggle_baseline()
