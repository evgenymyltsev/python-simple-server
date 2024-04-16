"""Provides a logger object with the specified name.

Module:
    logger

Attributes:
    name (str): The name of the logger.
"""

import json
import logging
import logging.config
import os


def get_logger(name: str) -> logging.Logger:
    """Return a logger object with the specified name.

    Args:
        name (str): The name of the logger.

    Raises:
        FileNotFoundError: If the log directory 'log' does not exist.

    Returns:
        logging.Logger: A logger object.
    """
    if not os.path.exists("log"):
        raise FileNotFoundError("Log directory 'log' does not exist. Please create it before using get_logger.")

    with open("logger.json") as f:
        config = json.load(f)
        config["loggers"][name] = config["loggers"]
    logging.config.dictConfig(config)
    return logging.getLogger(name)
