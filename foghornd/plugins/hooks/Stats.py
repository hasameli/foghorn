""" base --- hooks for foghornd """

import logging
from foghornd.plugins.hooks import HooksBase
from datetime import datetime, timedelta

"""
This module exposes hooks allowing plugins to extend the
functionality of foghorn.  This base module contains stubs of all the
hooks available.  Please check the documentation for each hook for
more information
"""


class Stats(HooksBase):
    """Hooks for foghorn"""
    last = {}
    lists = {}
    timeout = 60  # How often to print messages

    class TimedList(list):
        def __init__(self, timeout=60):
            self.timeout = timeout

        def _clearold(self):
            oldtime = datetime.now() - timedelta(seconds=self.timeout)
            self[:] = [x for x in self if x["time"] > oldtime]

        def append(self, obj):
            list.append(self, {"time": datetime.now(), "obj": obj})
            self._clearold()

    def checkstat(self, name):
        try:
            self.lists[name].append(1)
        except KeyError:
            self.lists[name] = self.TimedList()
            self.lists[name].append(1)

        try:
            self.last[name]
        except KeyError:
            self.last[name] = datetime.now() - timedelta(seconds=self.timeout)
        finally:
            if datetime.now() - timedelta(seconds=self.timeout) > self.last[name]:
                self.foghorn.logging.info("{} rate: {} per minute".format(name,  len(self.lists[name])))
                self.last[name] = datetime.now()

    def query(self, peer, query):
        """Called for every query before processing"""
        self.checkstat("query")

    def failed_acl(self, peer, query):
        """A query has failed the ACL"""
        self.checkstat("failed_acl")

    def no_acl(self, peer, query):
        """A query type has no ACL"""
        self.checkstat("no_acl")

    def passed(self, peer, query):
        """A query type has passed greylisting"""
        self.checkstat("passed")

    def upstream_error(self, peer, query):
        """Failure resolving this query"""
        self.checkstat("upstream_error")

    def sinkhole(self, peer, query):
        """A query will be sinkholed"""
        self.checkstat("sinkhole")

    def refused(self, peer, query):
        """A query has been refused"""
        self.checkstat("refused")

    def whitelist(self, peer, query):
        """A query has passed the whitelist"""
        self.checkstat("whitelist")

    def blacklist(self, peer, query):
        """A query has failed the blacklist"""
        self.checkstat("blacklist")

    def greylist_passed(self, peer, query, msg):
        """A query has failed the blacklist"""
        self.checkstat("greylist_passed")

    def greylist_failed(self, peer, query, msg):
        """A query has failed the blacklist"""
        self.checkstat("greylist_failed")

    def cache(self, query):
        self.checkstat("cache")
