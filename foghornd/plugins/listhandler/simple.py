from datetime import datetime
from foghornd.plugins.listhandler import ListHandlerBase

import dateutil.parser
import logging


class simple(ListHandlerBase):
    def __init__(self, settings):
        self.settings = settings
        self.logging = logging.getLogger('foghornd')
        print "Initing simple"

    def load_lists(self, signal_recvd=None, frame=None):
        """Load the white|grey|black lists"""
        # Signal handling
        # pylint: ignore=W0613
        self.whitelist = set(load_list(self.settings.whitelist_file))
        self.blacklist = set(load_list(self.settings.blacklist_file))
        self.greylist = {}

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
        key = query.name.name
        if key in self.whitelist:
            return True
        return False

    def check_blacklist(self, query):
        """Check the blacklist for this query"""
        key = query.name.name
        if key in self.blacklist:
            return True
        return False

    def check_greylist(self, query, baseline, peer_address):
        """Check the greylist for this query"""
        key = query.name.name
        curtime = datetime.now()
        if key in self.greylist:
            # Key exists in greylist
            entry = self.greylist[key]
            if (curtime - self.settings.grey_out) >= entry.first_seen:
                # Is the entry in the greyout period?
                if curtime - self.settings.blackout <= entry.last_seen:
                    # Is the entry in the blackout period?
                    self.logging.debug('Allowed by greylist %s ref-by %s',
                                       key, peer_address)
                    return True
                else:
                    self.logging.debug('Rejected/timeout by greylist %s ref-by %s',
                                       key, peer_address)
                    entry.first_seen()
                    entry.last_seen()
                    self.save_state()
                    return False
            else:
                self.logging.debug('Rejected/greyout by greylist %s ref-by %s',
                                   key, peer_address)
                return False
        else:
            # Entry not found in any list, so add it
            self.logging.debug('Rejected/notseen by greylist %s ref-by %s',
                               key, peer_address)
            if baseline:
                self.greylist[key] = GreylistEntry(key,
                                                   curtime - self.settings.grey_out)
                self.save_state()
                return True
            else:
                self.greylist[key] = GreylistEntry(key)
                self.save_state()
                return False


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


class GreylistEntry(object):
    """This class defines greylist entries"""

    def __init__(self, dns_field=None, first_seen=datetime.now(), last_seen=datetime.now()):
        self._dns_field = dns_field
        self._first_seen = first_seen
        self._last_seen = last_seen

    @property
    def dns_field(self):
        """Get dns_field"""
        return self._dns_field

    @dns_field.setter
    def dns_field(self, value):
        #TODO: this needs logic to define acceptable DNS names
        if len(value) <= 255:
            self._dns_field = value
            return True
        else:
            return False

    @property
    def first_seen(self):
        """Get first_seen"""
        return self._first_seen

    @first_seen.setter
    def first_seen(self, value=datetime.now()):
        self._first_seen = value

    @property
    def last_seen(self):
        """Get last_seen"""
        return self._last_seen

    @last_seen.setter
    def set_last_seen(self, value=datetime.now()):
        self._last_seen = value

    def __repr__(self):
        return "%s, %s, %s", self._dns_field, self._first_seen, self._last_seen
