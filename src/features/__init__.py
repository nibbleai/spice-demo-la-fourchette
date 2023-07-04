import logging

from spice import spice_logging_handler

logger = logging.getLogger()
logger.addHandler(spice_logging_handler)
logger.setLevel(logging.DEBUG)
