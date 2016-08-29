""" File --- FileHandler logger.  writes to settings.logfile """

import logging
from foghornd.plugins.logger import Logger


class File(Logger):
    """Logging for foghorn"""

    def __init__(self, settings):
        super(File, self).__init__(settings)

        file_handle = logging.FileHandler(settings.logfile)
        file_handle.setLevel(logging.DEBUG)
        file_handle.setFormatter(self.formatter)
        self.logger.addHandler(file_handle)
