import logging
import sys

def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    if logger.handlers:
        return
    logger.setLevel(level)
    h = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("[%(asctime)s] %(processName)s %(levelname)s %(name)s: %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
