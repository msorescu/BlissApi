__author__ = 'msorescu'

import logging
import logger
from config import Config


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


config = Config()
region = config.region
log = logging.getLogger('bliss')
log.addHandler(NullHandler())
logger.setup_logging(filename='/var/log/bliss.log', loglevel=config.log_level)
