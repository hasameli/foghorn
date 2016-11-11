"""FogHorn - DNS Greylisting"""

import logging
import signal
import sys

from datetime import datetime

from twisted.internet import defer
from twisted.names import dns, error, client

from foghornd.greylistentry import GreylistEntry
from foghornd.plugin_manager import PluginManager
from twisted.python import log
from foghornd.plugins.hooks import HooksBase
from foghornd.ACL import ACL


class Foghorn(object):
    """Manage lists of greylist entries and handles the list checks."""
    _peer_address = None
    baseline = False
    hook_types = ["init", "query", "failed_acl", "no_acl",
                  "passed", "upstream_error", "sinkhole", "refused",
                  "whitelist", "blacklist", "greylist_passed", "greylist_failed",
                  "cache"]
    hooks = {}
    acl_map = {dns.A: "allow_a", dns.AAAA: "allow_aaaa",
               dns.MX: "allow_mx", dns.SRV: "allow_srv",
               dns.PTR: "allow_ptr"}

    resolver = None

    def __init__(self, settings):
        self.settings = settings
        self.init_logging()
        self.baseline = self.settings.baseline
        self.logging = logging.getLogger('foghornd')
        signal.signal(signal.SIGUSR1, self.toggle_baseline)
        signal.signal(signal.SIGHUP, self.reload)
        self.init_listhandler()
        self.ACL = ACL(settings)

        if settings.resolver:
            upstream_servers = [tuple(l) for l in settings.resolver]
            self.resolver = client.Resolver(servers=upstream_servers)
        else:
            self.resolver = client.Resolver(resolv="/etc/resolv.conf")

        self.init_hooks()
        self.run_hook("init")

    def init_logging(self):
        self.logger_manager = PluginManager("foghornd.plugins.logger",
                                            "./foghornd/plugins/logger/",
                                            "*.py",
                                            "Logger")
        for logger in self.settings.loggers:
            self.logger_manager.new(logger, self.settings)

    def init_listhandler(self):
        self.listhandler_manager = PluginManager("foghornd.plugins.listhandler",
                                                 "./foghornd/plugins/listhandler/",
                                                 "*.py",
                                                 "ListHandlerBase")
        self.listhandler = self.listhandler_manager.new(self.settings.loader, self.settings)
        self.listhandler.load_lists()

    def init_hooks(self):
        for hook_type in self.hook_types:
            self.hooks[hook_type] = []

        self.hooks_manager = PluginManager("foghornd.plugins.hooks",
                                           "./foghornd/plugins/hooks/",
                                           "*.py",
                                           "HooksBase")
        if self.settings.hooks:
            for hook in self.settings.hooks:
                hook_obj = self.hooks_manager.new(hook, self.settings, self)
                for hook_type in self.hook_types:
                    # If the class has not been explicitly defined skip it.
                    is_baseclass = getattr(hook_obj.__class__, hook_type) == \
                                   getattr(HooksBase, hook_type)
                    if is_baseclass:
                        continue

                    caller = getattr(hook_obj, hook_type, None)
                    if caller:
                        self.hooks[hook_type].append(caller)

    def run_hook(self, hook, *args):
        for func in self.hooks[hook]:
            func(*args)

    # Signal handlers
    def reload(self, signal_recvd=None, frame=None):
        """Tell the white/black/greylist handler to reload"""
        # pylint: disable=W0613
        self.listhandler.load_lists()

    def toggle_baseline(self, signal_recvd=None, frame=None):
        """Toggle baselining - accepting all hosts to build greylist"""
        # pylint: disable=W0613
        self.logging.info('toggling baseline from %r to %r', self.baseline, not self.baseline)
        self.baseline = not self.baseline

    # API Functions
    def query_host(self, host):
        return self.listhandler.query_host(host)

    def query_all_lists(self):
        return self.listhandler.query_all_lists()

    def query_greylist(self):
        return self.listhandler.query_greylist()

    def query_blacklist(self):
        return self.listhandler.query_blacklist()

    def query_whitelist(self):
        return self.listhandler.query_whitelist()

    # Adders
    def add_to_whitelist(self, host, tag=None):
        self.listhandler.add_to_whitelist(host, tag)

    def add_to_blacklist(self, host, tag=None):
        self.listhandler.add_to_blacklist(host, tag)

    def add_to_greylist(self, host, tag=None):
        self.listhandler.add_to_greylist(host, tag)

    # Delete a host
    def delete_from_whitelist(self, host):
        self.listhandler.delete_from_whitelist(host)

    def delete_from_blacklist(self, host):
        self.listhandler.delete_from_blacklist(host)

    def delete_from_greylist(self, host, tag=None):
        self.listhandler.delete_from_greylist(host)

    # Delete a tag
    def delete_tag_from_whitelist(self, host):
        self.listhandler.delete_tag_from_whitelist(host)

    def delete_tag_from_blacklist(self, host):
        self.listhandler.delete_tag_from_blacklist(host)

    def delete_tag_from_greylist(self, host, tag=None):
        self.listhandler.delete_tag_from_greylist(host)

    # End API

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
        if query.type in [dns.A, dns.AAAA, dns.MX, dns.SRV, dns.PTR]:
            if self.listhandler.check_whitelist(query):
                self.run_hook("whitelist", self.peer_address, query)
                return True
            elif self.listhandler.check_blacklist(query):
                self.run_hook("blacklist", self.peer_address, query)
                return False
            else:
                log_msg = ""
                entry = self.listhandler.check_greylist(query, self.baseline, self.peer_address)
                ret_value = False
                if entry and not self.baseline:
                    entry.last_seen = curtime
                    response = entry.check_greyout(curtime, self.settings)
                    ret_value = response["ret_value"]
                    message = response["message"]
                    log_msg = "%s ref-by %s" % (message, self.peer_address)
                else:
                    # Entry not found in any list, so add it
                    if self.baseline:
                        log_msg = "Allowed by baseline by %s ref-by %s", (key, self.peer_address)
                        entry = GreylistEntry(key, curtime - self.settings.grey_out, curtime)
                        ret_value = True
                    else:
                        log_msg = "Rejected/notseen by greylist %s ref-by %s" % (key, self.peer_address)
                        entry = GreylistEntry(key)
                        ret_value = False

                if ret_value:
                    self.run_hook("greylist_passed", self.peer_address, query, log_msg)
                else:
                    self.run_hook("greylist_failed", self.peer_address, query, log_msg)

                self.listhandler.update_greylist(entry)
                return ret_value

    def build_response(self, query):
        """Build sinkholed response when disallowing a response."""
        name = query.name.name

        if query.type == dns.AAAA:
            answer = dns.RRHeader(name=name,
                                  type=dns.AAAA,
                                  payload=dns.Record_AAAA(address=b'%s' % self.settings.sinkhole6))
        elif query.type == dns.A:
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
        # ACL:
        try:
            if not self.ACL.check_acl(self.acl_map[query.type],
                                      self.peer_address.host):
                # Failed the ACL, refuse to answer
                self.run_hook("failed_acl", self.peer_address, query)
                return defer.fail(error.DNSQueryRefusedError())
        except KeyError:
            # Refuse to answer if we have no ACL for this type.
            # All non A, AAAA, MX, and SRV records fall here
            self.run_hook("no_acl", self.peer_address, query)
            return defer.fail(error.DNSQueryRefusedError())

        # FogHorn Greylisting:
        if self.list_check(query):
            # We've passed Foghorn!  Now we actually resolve the request
            self.run_hook("passed", self.peer_address, query)
            orig = log.msg
            try:
                log.msg = ignoremsg
                return self.resolver.query(query, timeout)
            except:
                self.run_hook("upstream_error", self.peer_address, query)

            log.msg = orig
        elif self.sinkholeable(query):
            # We've been requested to sinkhole this query
            self.run_hook("sinkhole", self.peer_address, query)
            return self.build_response(query)
        else:
            # No sinkhole defined, refuse to answer
            self.run_hook("refused", self.peer_address, query)
            return defer.fail(error.DNSQueryRefusedError())

    def sinkholeable(self, query):
        return ((query.type == dns.A and self.settings.sinkhole) or
                (query.type == dns.AAAA and self.settings.sinkhole6))


def ignoremsg(*args):
    pass
