"""This is the logging module for the main app."""
import os
import logging
from datetime import datetime as dt
from logging.config import dictConfig
import yaml


def make_logger(logFileName):
    """Creates a logger that saves to a custom log file location."""
    # Import the configuration from logging_config.yml
    python_package_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(python_package_dir, 'logging_config.yml'), 'r') as config_file:
        config = yaml.safe_load(config_file)
        # Edit the log file location to the input of the function
        config['handlers']['file']['filename'] = logFileName
    # Configure the logger with the configurtion
    dictConfig(config)
    # Instantiate our configurated logger
    logger = logging.getLogger()
    return logger

logger = make_logger(os.path.join("logs", str(dt.today().date()) + "_mm.log"))

if __name__ == "__main__":
    make_logger(os.path.join("logs", str(dt.today().date()) + "_mm.log"))