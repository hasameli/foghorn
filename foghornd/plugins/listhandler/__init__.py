""" base -- Abstract Base Class for plugins of type """

import logging
from abc import ABCMeta, abstractmethod


class ListHandlerBase():
    """Interface"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, settings):
        self.settings = settings
        self.logging = logging.getLogger('foghornd')

    @abstractmethod
    def load_lists(self, signal_recvd=None, frame=None):
        """Load the white|grey|black lists"""

    @abstractmethod
    def save_state(self):
        """Called as the program is shutting down, put shut down tasks here."""

    @abstractmethod
    def check_whitelist(self, query):
        """Check the whitelist for this query"""

    @abstractmethod
    def check_blacklist(self, query):
        """Check the blacklist for this query"""

    @abstractmethod
    def check_greylist(self, query, baseline, peer_address):
        """Check the greylist for this query"""

    @abstractmethod
    def update_greylist(self, entry):
        """update the greylist with this entry"""
