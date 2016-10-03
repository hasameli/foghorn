"""Store lists in flat files on to disk and read into memory"""

import logging
import dateutil.parser

from foghornd.plugins.listhandler import ListHandlerBase
from foghornd.greylistentry import GreylistEntry


class Simple(ListHandlerBase):
    """Simple ListHandler"""

    whitelist = {}
    blacklist = {}
    greylist = {}

    def __init__(self, settings):
        super(Simple, self).__init__(settings)
        self.settings = settings
        self.logging = logging.getLogger('foghornd')

    def load_lists(self, signal_recvd=None, frame=None):
        """Load the white|grey|black lists"""
        # Signal handling
        # pylint: disable=W0613
        for item in load_list(self.settings.whitelist_file):
            self.whitelist[item] = 'whitelistfile'

        for item in load_list(self.settings.blacklist_file):
            self.blacklist[item] = 'blacklistfile'

        for item in load_list(self.settings.greylist_file):
            elements = [n.strip() for n in item.split(',')]
            if len(elements) == 3:
                entry = GreylistEntry(
                    elements[0],
                    dateutil.parser.parse(elements[1]),
                    dateutil.parser.parse(elements[2])
                )
                self.greylist[elements[0]] = entry
            else:
                self.logging.debug('Error processing line: %s', item)

    def save_state(self):
        """Called as the program is shutting down, put shut down tasks here."""
        write_list(self.settings.greylist_file, self.greylist)

    def check_whitelist(self, query):
        """Check the whitelist for this query"""
        try:
            self.whitelist[query.name.name]
            return True
        except KeyError:
            return False

    def check_blacklist(self, query):
        """Check the blacklist for this query"""
        try:
            self.blacklist[query.name.name]
            return True
        except KeyError:
            return False

    def check_greylist(self, query, baseline, peer_address):
        """Check the greylist for this query"""
        try:
            return self.greylist[query.name.name]
        except KeyError:
            return False

    def update_greylist(self, entry):
        key = entry.dns_field
        self.greylist[key] = entry
        self.save_state()

    def add_to_whitelist(self, host, tag=1):
        self.whitelist[host] = tag

    def add_to_blacklist(self, host, tag=1):
        self.blacklist[host] = tag

    def add_to_greylist(self, host, tag=1):
        self.greylist[host] = tag

    def delete_from_whitelist(self, host):
        del self.whitelist[host]

    def delete_from_greylist(self, host):
        del self.greylist[host]

    def delete_from_blacklist(self, host):
        del self.blacklist[host]

    def delete_tag_from_whitelist(self, tag):
        for key in self.whitelist:
            if self.whitelist[key] == tag:
                del self.whitelist[key]

    def delete_tag_from_greylist(self, tag):
        for key in self.greylist.keys():
            if self.greylist[key] == tag:
                del self.greylist[key]

    def delete_tag_from_blacklist(self, tag):
        for key in self.blacklist.keys():
            if self.blacklist[key] == tag:
                del self.blacklist[key]

    def query_blacklist(self):
        return [self.blacklist.keys()]

    def query_whitelist(self):
        return [self.blacklist.keys()]

    def query_greylist(self):
        return [self.greylist.keys()]


def write_list(filename, items):
    """Write out [gray|whit|black] blists"""
    greylist_entries = False
    if len(items.keys()) > 0 and isinstance(items.itervalues().next(), GreylistEntry):
        greylist_entries = True
    else:
        # We're not going to support writing the other lists at the moment
        return False

    try:
        with open(filename, mode='w') as write_file:
            if greylist_entries:
                for item in items.itervalues():
                    write_file.write(format("%s,%s,%s\n" %
                                            (item.dns_field, item.first_seen, item.last_seen)))
                    return True
    except IOError as io_error:
        print "%s" % io_error
        return False


def load_list(filename):
    """Load the specified list."""
    lines = []
    try:
        with open(filename, mode='r') as read_file:
            lines = [x.strip() for x in read_file.readlines()]
            return lines
    except IOError as io_error:
        print "%s" % io_error
        return []
