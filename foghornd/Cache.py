#!/usr/bin/env python

"""Cache"""

from twisted.names.cache import CacheResolver


class Cache(CacheResolver):

    foghorn = None
    peer_address = None

    def query(self, query, timeout=0):
        self.foghorn.run_hook("query", self.peer_address, query)
        resp = CacheResolver.query(self, query, timeout)
        if resp and self.foghorn:
            self.foghorn.run_hook("cache", query)
        return resp
