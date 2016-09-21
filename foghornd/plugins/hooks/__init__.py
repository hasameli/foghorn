""" base --- hooks for foghornd """

import logging

"""
This module exposes hooks allowing plugins to extend the
functionality of foghorn.  This base module contains stubs of all the
hooks available.  Please check the documentation for each hook for
more information
"""


class HooksBase(object):
    """Hooks for foghorn"""

    def __init__(self, settings, foghorn):
        """Each object holds a copy of the settings and a logger"""
        self.settings = settings
        self.logger = logging.getLogger('foghornd')
        self.foghorn = foghorn

    def init(self):
        """Called on startup"""
        pass
