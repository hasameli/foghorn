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

    def xmlrpc_reload_lists(self):
        self.foghorn.reload()

    def xmlrpc_query_host(self, host):
        res = self.foghorn.query_host(host)
        self.foghorn.logging.error(res)
        return res

    def xmlrpc_add_to_whitelist(self, host, tag=None):
        self.foghorn.add_to_whitelist(host, tag)

    def xmlrpc_add_to_blacklist(self, host, tag=None):
        self.foghorn.add_to_blacklist(host, tag)

    def xmlrpc_add_to_greylist(self, host, tag=None):
        self.foghorn.add_to_greylist(host, tag)

    def xmlrpc_delete_from_whitelist(self, host):
        self.foghorn.delete_from_whitelist(host)

    def xmlrpc_delete_from_blacklist(self, host):
        self.foghorn.delete_from_blacklist(host)

    def xmlrpc_delete_from_greylist(self, host):
        self.foghorn.delete_from_greylist(host)

    def xmlrpc_delete_tag_from_whitelist(self, tag):
        self.foghorn.delete_tag_from_whitelist(tag)

    def xmlrpc_delete_tag_from_blacklist(self, tag):
        self.foghorn.delete_tag_from_blacklist(tag)

    def xmlrpc_delete_tag_from_greylist(self, tag):
        self.foghorn.delete_tag_from_greylist(tag)
