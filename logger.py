import json
import logging
import logging.config
import os


def create_log_folder() -> None:
    if not os.path.exists("log"):
        os.mkdir("log")


def get_logger(name: str) -> logging.Logger:
    create_log_folder()
    with open("logger.json") as f:
        config = json.load(f)
        config["loggers"][name] = config["loggers"]
    logging.config.dictConfig(config)
    return logging.getLogger(name)
