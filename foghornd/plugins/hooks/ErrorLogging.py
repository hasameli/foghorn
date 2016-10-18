""" base --- hooks for foghornd """

import logging
from foghornd.plugins.hooks import HooksBase

"""
This module exposes hooks allowing plugins to extend the
functionality of foghorn.  This base module contains stubs of all the
hooks available.  Please check the documentation for each hook for
more information
"""


class ErrorLogging(HooksBase):
    """Hooks for foghorn"""

    def failed_acl(self, peer, query):
        """A query has failed the ACL"""
        logger = self.foghorn.logging.warn
        logger("Failed ACL: %s - %s" % (peer, query))

    def no_acl(self, peer, query):
        """A query type has no ACL"""
        logger = self.foghorn.logging.warn
        logger("no_acl: %s - %s" % (peer, query))

    def upstream_error(self, peer, query):
        """Failure resolving this query"""
        logger = self.foghorn.logging.error
        logger("upstream_error: %s - %s" % (peer, query))

    def blacklist(self, peer, query):
        """A query has failed the blacklist"""
        logger = self.foghorn.logging.debug
        logger("blacklist: %s - %s" % (peer, query))

    def greylist_failed(self, peer, query, msg):
        """A query has failed the blacklist"""
        logger = self.foghorn.logging.debug
        logger("greylist_failed: %s - %s - %s" % (peer, query, msg))
