"""FogHorn - DNS Greylisting"""

import logging
import signal

from twisted.internet import defer
from twisted.names import dns, error

from foghornd.greylistentry import GreylistEntry
from foghornd.plugin_manager import PluginManager

from datetime import datetime

class Foghorn(object):
    """Manage lists of greylist entries and handles the list checks."""
    _peer_address = None
    baseline = False

    def __init__(self, settings):
        self.settings = settings
        self.logging = logging.getLogger('foghornd')
        signal.signal(signal.SIGUSR1, self.toggle_baseline)
        signal.signal(signal.SIGHUP, self.reload)
        self.listhandler_manager = PluginManager("foghornd.plugins.listhandler",
                                                 "./foghornd/plugins/listhandler/")
        self.listhandler = self.listhandler_manager.new(self.settings.loader, self.settings)
        self.listhandler.load_lists()

    # Signal handlers
    def reload(self, signal_recvd=None, frame=None):
        # pylint: ignore=W0613
        self.listhandler.load_lists()

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
        key = query.name.name
        curtime = datetime.now()
        if query.type in [dns.A, dns.AAAA]:
            if self.listhandler.check_whitelist(query):
                self.logging.debug('Allowed by whitelist %s ref-by %s', key, self.peer_address)
                return True
            elif self.listhandler.check_blacklist(query):
                self.logging.debug('Rejected by blacklist %s ref-by %s', key, self.peer_address)
                return False
            else:
                entry = self.listhandler.check_greylist(query,self.baseline, self.peer_address)
                ret_value = False
                if entry:
                    entry.last_seen = curtime
                    if (curtime - self.settings.grey_out) >= entry.first_seen:
                        # Is the entry in the greyout period?
                        if curtime - self.settings.blackout <= entry.last_seen:
                            # Is the entry in the blackout period?
                            self.logging.debug('Allowed by greylist %s ref-by %s',
                                               key, self.peer_address)
                            ret_value = True
                        else:
                            self.logging.debug('Rejected/timeout by greylist %s ref-by %s',
                                               key, self.peer_address)
                            ret_value = False
                    else:
                        self.logging.debug('Rejected/greyout by greylist %s ref-by %s',
                                           key, self.peer_address)
                        ret_value = False
                else:
                    # Entry not found in any list, so add it
                    self.logging.debug('Rejected/notseen by greylist %s ref-by %s',
                                       key, self.peer_address)
                    if self.baseline:
                        entry = GreylistEntry(key, curtime - self.settings.grey_out)
                        ret_value = True
                    else:
                        entry = GreylistEntry(key)
                        ret_value = False
                self.listhandler.update_greylist(entry)
                return ret_value

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
