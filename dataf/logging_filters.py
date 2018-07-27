#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Logging filters
---------------

Custom filters for logging

"""

import logging


class LvlFilter(logging.Filter):
    """
    Custom filter based on level.
    """
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def filter(self, record):
        return self.low <= record.levelno <= self.high
