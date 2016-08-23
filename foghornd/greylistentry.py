from datetime import datetime


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
    def last_seen(self, value=datetime.now()):
        self._last_seen = value

    def __repr__(self):
        return "%s, %s, %s", self._dns_field, self._first_seen, self._last_seen
