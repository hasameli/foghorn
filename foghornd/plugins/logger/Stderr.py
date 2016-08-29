""" Stderr --- log to STDERR.  Takes no options """

import logging
from foghornd.plugins.logger import Logger


class Stderr(Logger):
    """Logging for foghorn"""

    def __init__(self, settings):
        super(Stderr, self).__init__(settings)

        log_streamhandler = logging.StreamHandler()
        log_streamhandler.setLevel(logging.DEBUG)
        log_streamhandler.setFormatter(self.formatter)
        self.logger.addHandler(log_streamhandler)
