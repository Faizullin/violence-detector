import logging


def get_logger(name: str = "API", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
