from os import environ
import logging

from logzero import setup_logger

# https://docs.python.org/3/library/logging.html#logging-levels
loglevel: int = logging.DEBUG  # (10)
if "LOLEXPORT" in environ:
    loglevel = int(environ["LOLEXPORT"])

# logzero handles this fine, can be imported/configured
# multiple times
logger = setup_logger(name="lolexport", level=loglevel)
