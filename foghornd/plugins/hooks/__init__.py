""" base --- hooks for foghornd """

import logging

"""
This module exposes hooks allowing plugins to extend the
functionality of foghorn.  This base module contains stubs of all the
hooks available.  Please check the documentation for each hook for
more information
"""


class HooksBase(object):
    """Hooks for foghorn"""

    def __init__(self, settings, foghorn):
        """Each object holds a copy of the settings and a logger"""
        self.settings = settings
        self.logger = logging.getLogger('foghornd')
        self.foghorn = foghorn

    def init(self):
        """Called on startup"""
        pass

    def query(self, peer, query):
        """Called for every query before processing"""
        pass

    def failed_acl(self, peer, query):
        """A query has failed the ACL"""
        pass

    def no_acl(self, peer, query):
        """A query type has no ACL"""
        pass

    def passed(self, peer, query):
        """A query type has passed greylisting"""
        pass

    def upstream_error(self, peer, query):
        """Failure resolving this query"""
        pass

    def sinkhole(self, peer, query):
        """A query will be sinkholed"""
        pass

    def refused(self, peer, query):
        """A query has been refused"""
        pass

    def whitelist(self, peer, query):
        """A query has passed the whitelist"""
        pass

    def blacklist(self, peer, query):
        """A query has failed the blacklist"""
        pass

    def greylist_passed(self, peer, query, msg):
        """A query has failed the blacklist"""
        pass

    def greylist_failed(self, peer, query, msg):
        """A query has failed the blacklist"""
        pass
