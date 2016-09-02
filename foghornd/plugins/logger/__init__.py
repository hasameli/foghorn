""" base --- base logging class """

import logging


class Logger(object):
    """Logging for foghorn"""

    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger('foghornd')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s")
