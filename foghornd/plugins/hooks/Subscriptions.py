""" base --- hooks for foghornd """

import requests
import re
from foghornd.plugins.hooks import HooksBase

"""
This module exposes hooks allowing plugins to extend the
functionality of foghorn.  This base module contains stubs of all the
hooks available.  Please check the documentation for each hook for
more information
"""


class Subscriptions (HooksBase):
    """Hooks for foghorn"""

    def init(self):
        """Called on startup"""
        dispatch = {"json": self.process_json,
                    "hostfile": self.process_hostfile}

        for subscription in self.settings.loader_settings["subscriptions"]:
            response = requests.get(subscription["url"])

            if "delete" in subscription.keys() and "tag" in subscription.keys():
                self.foghorn.delete_tag_from_whitelist(subscription["tag"])
                self.foghorn.delete_tag_from_greylist(subscription["tag"])
                self.foghorn.delete_tag_from_blacklist(subscription["tag"])

            dispatch[subscription["type"]](subscription, response)

    def process_json(self, subscription, response):
        """
        Parses a json response of a dict of lists of strings.
        eg: { "whitelist": [ "www.google.com" ], "blacklist": [ "www.bing.com" ] }
        """
        items = response.json()

        if "whitelist" in items.keys():
            for host in items["whitelist"]:
                self.foghorn.add_to_whitelist(host, subscription["tag"])

        if "greylist" in items.keys():
            for host in items["greylist"]:
                self.foghorn.add_to_greylist(host, subscription["tag"])

        if "blacklist" in items.keys():
            for host in items["blacklist"]:
                self.foghorn.add_to_blacklist(host, subscription["tag"])

    def process_hostfile(self, subscription, response):
        """
        Very basic hostfile parser.  Only supports one host per line.
        If the host is mapped to an ip in addips it is added to the blacklist
        """
        items = response.text
        addips = ["0.0.0.0", "127.0.0.1"]
        for item in items.split("\n"):
            clean_line = re.sub('#.*','',item)
            if not item:
                continue

            row = clean_line.split(" ")
            if len(row) < 2:
                continue
            if row[0] in addips:
                self.foghorn.add_to_blacklist(row[1], subscription["tag"])
