#!/usr/bin/env python
import sys, os
from datetime import datetime


class greyList:

    dnsField = None
    firstSeen = None
    lastSeen = None
#    """This class defines grey lists"""
    
    def getDnsField(self):
        return self.dnsField

    def getFirstSeen(self):
        return self.firstSeen

    def getLastSeen(self):
        return self.lastSeen

    def setDnsField(self, dnsField):
#    """TODO: this needs logic to define acceptable DNS names"""
        if (len(dnsField) <= 255):
            self.dnsField = dnsField
            return True
        else:
            return False

    def setFirstSeen(self, firstSeen = datetime.now()):
        self.firstSeen = firstSeen

    def setLastSeen(self, lastSeen = datetime.now()):
        self.lastSeen = lastSeen

    def createListEntry(self, dnsField, firstSeen = datetime.now(), lastSeen = datetime.now()):
        self.setDnsField(dnsField)
        self.setFirstSeen(firstSeen)
        self.setLastSeen(lastSeen)

    def __str__(self):
        return "%s, %s, %s".format(self.dnsField, self.firstSeen, self.lastSeen)



