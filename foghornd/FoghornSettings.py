'''Configuration settings for Foghorn.'''

import atexit
import json
import os

from datetime import timedelta


class FoghornSettings(object):
    '''Default settings for Foghorn'''

    # PATHS
    home = os.path.dirname(__file__)
    path = os.path.join(home, "settings.json")
    WhitelistFile = os.path.join(home, "greydns", "whitelist")
    BlacklistFile = os.path.join(home, "greydns", "blacklist")
    GreylistFile = os.path.join(home, "greydns", "greylist")

    def __init__(self):
        super(FoghornSettings, self).__init__()

        self.data = {}
        self.load()
        atexit.register(self.save)

    def load(self):
        '''Load settings'''

        with open(self.path) as f:
            self.data.update(json.load(f))

    def save(self):
        '''Save settings'''

        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

    # PROPERTIES
    # ----------

    @property
    def logfile(self):
        return self.data.get("logfile", "foghornd.log")

    @logfile.setter
    def logfile(self, value):
        self.data["logfile"] = value

    @property
    def DNSServerIP(self):
        return self.data.get("dns_server_ip", "192.168.1.1")

    @DNSServerIP.setter
    def DNSServerIP(self, value):
        self.data["dns_server_ip"] = value

    @property
    def GreyIP(self):
        return self.data.get("grey_ip", "192.168.5.1")

    @GreyIP.setter
    def GreyIP(self, value):
        self.data["grey_ip"] = value

    @property
    def DNSPort(self):
        """Local port number to listen on"""

        return self.data.get("dns_port", 10053)

    @DNSPort.setter
    def DNSPort(self, value):
        self.data["dns_port"] = value

    @property
    def Sinkhole(self):
        """Sinkhole IP for black/greylisting"""

        return self.data.get("sinkhole", "127.0.0.1")

    @Sinkhole.setter
    def Sinkhole(self, value):
        self.data["sinkhole"] = value

    @property
    def GreyOut(self):
        """Time from firstseen to first allowed"""

        return timedelta(hours=self.data.get("greyout", 24))

    @GreyOut.setter
    def GreyOut(self, value):
        """Convert deltatime to hours"""

        self.data["greyout"] = value.total_seconds() / 3600.

    @property
    def BlackOut(self):
        """Time from lastseen after which it is no longer allowed"""

        return timedelta(hours=self.data.get("blackout", 180))

    @BlackOut.setter
    def BlackOut(self, value):
        """Convert deltatime to hours"""

        self.data["blackout"] = value.total_seconds() / 3600.

    @property
    def RefreshPeriod(self):
        return timedelta(minutes=self.data.get("refresh", 5))

    @RefreshPeriod.setter
    def RefreshPeriod(self, value):
        """Convert deltatime to minutes"""

        self.data["refresh"] = value.total_seconds() / 60.
