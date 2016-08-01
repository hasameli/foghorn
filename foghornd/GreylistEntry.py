from datetime import datetime

class GreylistEntry(object):
    """This class defines greylist entries"""

    def __init__(self, dnsField = None, firstSeen = datetime.now(), lastSeen = datetime.now()):
        self._dnsField = dnsField
        self._firstSeen = firstSeen
        self._lastSeen = lastSeen

    @property
    def dnsField(self):
        return self._dnsField

    @dnsField.setter
    def dnsField(self, value):
        #TODO: this needs logic to define acceptable DNS names
        if len(value) <= 255:
            self._dnsField = value
            return True
        else:
            return False

    @property
    def firstSeen(self):
        return self._firstSeen

    @firstSeen.setter
    def firstSeen(self, value = datetime.now()):
        self._firstSeen = value

    @property
    def lastSeen(self):
        return self._lastSeen

    @lastSeen.setter
    def setLastSeen(self, value = datetime.now()):
        self._lastSeen = value

    def __repr__(self):
        return "%s, %s, %s" % (self._dnsField, self._firstSeen, self._lastSeen)

