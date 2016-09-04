""" base -- Abstract Base Class for plugins of type """

import logging
from abc import ABCMeta, abstractmethod
from twisted.names.dns import Query

class ListHandlerBase():
    """Interface"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, settings):
        self.settings = settings
        self.logging = logging.getLogger('foghornd')

    @abstractmethod
    def load_lists(self, signal_recvd=None, frame=None):
        """Load the white|grey|black lists"""

    @abstractmethod
    def save_state(self):
        """Called as the program is shutting down, put shut down tasks here."""

    @abstractmethod
    def check_whitelist(self, query):
        """Check the whitelist for this query"""

    @abstractmethod
    def check_blacklist(self, query):
        """Check the blacklist for this query"""

    @abstractmethod
    def check_greylist(self, query, baseline, peer_address):
        """Check the greylist for this query"""

    @abstractmethod
    def update_greylist(self, entry):
        """update the greylist with this entry"""

    # TODO: make these @abstractmethods after Simple is updated
    def add_to_whitelist(self, host, tag=None):
        self.logging.warn("add_to_whitelist not implemented in %s" % self.__class__)

    def add_to_blacklist(self, host, tag=None):
        self.logging.warn("add_to_blacklist not implemented in %s" % self.__class__)

    def add_to_greylist(self, host, tag=None):
        self.logging.warn("add_to_blacklist not implemented in %s" % self.__class__)

    def delete_from_whitelist(self, host):
        self.logging.warn("delete_from_whitelist not implemented in %s" % self.__class__)

    def delete_from_blacklist(self, host):
        self.logging.warn("delete_from_blacklist not implemented in %s" % self.__class__)

    def delete_from_greylist(self, host):
        self.logging.warn("delete_from_blacklist not implemented in %s" % self.__class__)

    def delete_tag_from_whitelist(self, host):
        self.logging.warn("delete_tag_from_whitelist not implemented in %s" % self.__class__)

    def delete_tag_from_blacklist(self, host):
        self.logging.warn("delete_tag_from_blacklist not implemented in %s" % self.__class__)

    def delete_tag_from_greylist(self, host):
        self.logging.warn("delete_tag_from_blacklist not implemented in %s" % self.__class__)

    # Implemented methods
    def query_host(self, host):
        query = Query(host)
        res = {}
        res["whitelist"] = self.check_whitelist(query)
        res["blacklist"] = self.check_blacklist(query)
        if self.check_greylist(query, None, None):
            res["greylist"] = True
        else:
            res["greylist"] = False
        return res
