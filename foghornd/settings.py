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
    # This should be split out somewhere else for the simple handler
    whitelist_file = os.path.join(home, "greydns", "whitelist")
    blacklist_file = os.path.join(home, "greydns", "blacklist")
    greylist_file = os.path.join(home, "greydns", "greylist")

    def __init__(self):
        super(FoghornSettings, self).__init__()

        self.data = {}
        self.load()
        atexit.register(self.save)

    def load(self):
        '''Load settings'''

        with open(self.path) as settings_file:
            self.data.update(json.load(settings_file))

    def save(self):
        '''Save settings'''

        with open(self.path, "w") as settings_file:
            json.dump(self.data, settings_file, indent=4, sort_keys=True)

    # PROPERTIES
    # ----------

    @property
    def logfile(self):
        """Return current logfile"""
        return self.data.get("logfile", "foghornd.log")

    @logfile.setter
    def logfile(self, value):
        self.data["logfile"] = value

    @property
    def dns_server_ip(self):
        """Return current dns server ip"""
        return self.data.get("dns_server_ip", "192.168.1.1")

    @dns_server_ip.setter
    def dns_server_ip(self, value):
        self.data["dns_server_ip"] = value

    @property
    def grey_ip(self):
        """Return current grey ip"""
        return self.data.get("grey_ip", "192.168.5.1")

    @grey_ip.setter
    def grey_ip(self, value):
        self.data["grey_ip"] = value

    @property
    def dns_port(self):
        """Local port number to listen on"""

        return self.data.get("dns_port", 10053)

    @dns_port.setter
    def dns_port(self, value):
        self.data["dns_port"] = value

    @property
    def sinkhole(self):
        """Sinkhole IP for black/greylisting"""

        return self.data.get("sinkhole", "127.0.0.1")

    @sinkhole.setter
    def sinkhole(self, value):
        self.data["sinkhole"] = value

    @property
    def sinkhole6(self):
        """Sinkhole IP for black/greylisting"""

        return self.data.get("sinkhole6", "::1")

    @sinkhole6.setter
    def sinkhole6(self, value):
        self.data["sinkhole6"] = value

    @property
    def grey_out(self):
        """Time from firstseen to first allowed"""

        return timedelta(hours=self.data.get("greyout", 24))

    @grey_out.setter
    def grey_out(self, value):
        """Convert deltatime to hours"""

        self.data["greyout"] = value.total_seconds() / 3600.

    @property
    def blackout(self):
        """Time from lastseen after which it is no longer allowed"""

        return timedelta(hours=self.data.get("blackout", 180))

    @blackout.setter
    def blackout(self, value):
        """Convert deltatime to hours"""

        self.data["blackout"] = value.total_seconds() / 3600.

    @property
    def refresh_period(self):
        """Return current refresh_period"""
        return timedelta(minutes=self.data.get("refresh", 5))

    @refresh_period.setter
    def refresh_period(self, value):
        """Convert deltatime to minutes"""

        self.data["refresh"] = value.total_seconds() / 60.

    @property
    def loader(self):
        """Return which loader to use"""
        return self.data.get("loader", "simple")

    @loader.setter
    def loader(self, value):
        self.data["loader"] = value

    @property
    def loader_settings(self):
        """Return settings for the loader"""
        return self.data.get("loader_settings", {})

    @loader_settings.setter
    def loader_settings(self, value):
        self.data["loader_settings"] = value

    @property
    def loggers(self):
        """Return settings for the loader"""
        return self.data.get("loggers", ["Stderr", "File"])

    @loggers.setter
    def loggers(self, value):
        self.data["loggers"] = value

    @property
    def logger_settings(self):
        """Return settings for the loader"""
        return self.data.get("logger_settings", {})

    @logger_settings.setter
    def logger_settings(self, value):
        self.data["logger_settings"] = value
