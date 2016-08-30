""" Syslog --- log to syslog. """

# FIXME: Add settings

import logging
from foghornd.plugins.logger import Logger
from logging.handlers import SysLogHandler

class Syslog(Logger):
    """Logging for foghorn"""

    def __init__(self, settings):
        super(Syslog, self).__init__(settings)
        option = settings.logger_settings["Syslog"]
        if option["socket"]:
            handler = SysLogHandler(address=option["socket"])
        else:
            handler = SysLogHandler(address=(option["host"], option["port"]))
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
