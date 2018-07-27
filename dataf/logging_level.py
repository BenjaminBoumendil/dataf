#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Logging level
-------------

Custom level for logging.

"""


class LoggingLevel:
    """
    Custom logging level.
    All method are static so they can dynamically inherit from the logger they are used by.

    :attr dict name_to_level: static dict to define reference between name and level.
    """
    name_to_level = {
        'SLACK': 60,
        'MAIL': 70,
    }

    @staticmethod
    def slack(self, message, *args, **kwargs):
        """
        Custon level for slack logging.
        """
        self._log(LoggingLevel.name_to_level['SLACK'], message, args, **kwargs)

    @staticmethod
    def mail(self, message, *args, **kwargs):
        """
        Custom level for mail logging.
        """
        self._log(LoggingLevel.name_to_level['MAIL'], message, args, **kwargs)
