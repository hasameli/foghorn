#!/usr/bin/env python

"""Cache"""

from twisted.names.cache import CacheResolver


class Cache(CacheResolver):

    foghorn = None

    def query(self, query, timeout=0):
        resp = CacheResolver.query(self, query, timeout)
        if resp and self.foghorn:
            self.foghorn.run_hook("cache", query)
        return resp
