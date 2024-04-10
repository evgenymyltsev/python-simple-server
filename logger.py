import json
import logging
import logging.config
import os

FOLDER_LOG = "log"
LOGGING_CONFIG_FILE = "loggers.json"


def create_log_folder(folder=FOLDER_LOG):
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name):
    create_log_folder()
    with open(LOGGING_CONFIG_FILE) as f:
        config = json.load(f)
        config["loggers"][name] = config["loggers"]
    logging.config.dictConfig(config)
    return logging.getLogger(name)
