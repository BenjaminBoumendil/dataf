#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Settings
--------

Global settings.

"""

import os
import logging
import logging.config
from collections import OrderedDict

from dataf import LoggingLevel, YamlParser


# Global settings variable, True for development and False for production
DEBUG = True

# Settings directory
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))

# Project root directory
ROOT_DIR = os.path.realpath(os.path.join(SETTINGS_DIR, '..'))

# Directory global
DIRECTORY = {}

# Database global
DATABASE = {}

# Logging global
LOGGING = {}

# Flask views
VIEWS = {}

# Swagger global
SWAGGER = {}


# Swagger settings func
def rule_filter(rule): return True


def model_filter(tag): return True


# Yaml section link to data struct
# !! Directory must be loaded first because of include in other yml !!
YAML_TO_DICT = OrderedDict([
    ('directory.yml', DIRECTORY),
    ('database.yml', DATABASE),
    ('logging.yml', LOGGING),
    ('views.yml', VIEWS),
    ('swagger.yml', SWAGGER),
])


def setup_logging():
    """
    Setup logging configuration.
    """
    # Setup custom logging level
    for name, level in LoggingLevel.name_to_level.items():
        logging.addLevelName(level, name)
        name_lower = name.lower()
        setattr(logging.Logger, name_lower, getattr(LoggingLevel, name_lower))
    # Load yaml config
    logging.config.dictConfig(LOGGING)


def create_directory():
    """
    Create directory.
    """
    for path_dir in DIRECTORY.values():
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)


YamlParser(DEBUG).add_getter_constructor(
    '!get_directory', DIRECTORY
).parse(YAML_TO_DICT, SETTINGS_DIR)
create_directory()
setup_logging()
