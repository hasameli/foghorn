"""FogHorn - DNS Greylisting"""

import logging
import signal

from twisted.internet import defer
from twisted.names import dns, error

from foghornd.plugin_manager import PluginManager


class Foghorn(object):
    """Manage lists of greylist entries and handles the list checks."""
    _peer_address = None
    baseline = False

    def __init__(self, settings):
        self.settings = settings
        self.logging = logging.getLogger('foghornd')
        signal.signal(signal.SIGUSR1, self.toggle_baseline)
        signal.signal(signal.SIGHUP, self.reload)
        self.loader_manager = PluginManager("foghornd.plugins.loader", "./foghornd/plugins/loader/")
        self.loader = self.loader_manager.new("simple", self.settings)
        self.loader.load_lists()

    # Signal handlers
    def reload(self,  signal_recvd=None, frame=None):
        # pylint: ignore=W0613
        self.loader.load_lists()

    def toggle_baseline(self, signal_recvd=None, frame=None):
        """Toggle baselining - accepting all hosts to build greylist"""
        # pylint: ignore=W0613
        self.logging.debug('toggling baseline from %r to %r', self.baseline, not self.baseline)
        self.baseline = not self.baseline

    @property
    def peer_address(self):
        """peer_address is injected in here for logging"""
        return self._peer_address

    @peer_address.setter
    def peer_address(self, value):
        self._peer_address = value

    def list_check(self, query):
        """
        Handle rules regarding what resolves by checking whether
        the record requested is in our lists. Order is important.
        """
        if query.type in [dns.A, dns.AAAA]:
            if self.loader.check_whitelist(query):
                self.logging.debug('Allowed by whitelist %s ref-by %s', key, self.peer_address)
                return True
            elif self.loader.check_blacklist(query):
                self.logging.debug('Rejected by blacklist %s ref-by %s', key, self.peer_address)
                return False
            else:
                return self.loader.check_greylist(query,self.baseline, self.peer_address)

    def build_response(self, query):
        """Build sinkholed response when disallowing a response."""
        name = query.name.name

        if query.type == dns.AAAA:
            answer = dns.RRHeader(name=name,
                                  type=dns.AAAA,
                                  payload=dns.Record_AAAA(address=b'%s' % self.settings.sinkhole6))
        else:
            answer = dns.RRHeader(name=name,
                                  payload=dns.Record_A(address=b'%s' % (self.settings.sinkhole)))
        answers = [answer]
        authority = []
        additional = []
        return answers, authority, additional

    def query(self, query, timeout=0):
        """
        Either return our fake response, or let it on through to the next resolver
        in the chain
        """
        # Disable the warning that timeout is unused. We have to
        # accept the argument.
        # pylint: disable=W0613
        if not self.list_check(query):
            return defer.succeed(self.build_response(query))
        else:
            return defer.fail(error.DomainError())
