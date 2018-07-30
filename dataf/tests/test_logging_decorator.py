#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Test logging decorator
----------------------

Test suite for logging_decorator.

"""

import logging
import unittest

from dataf import simple_logger, err_simple_logger, lambda_logger, err_lambda_logger


class LoggingTestMethod:
    logger = logging.getLogger(__name__)

    @simple_logger('debug', start='Start message', end='End message')
    def simple_logger_method(self):
        pass

    # @err_simple_logger()
    # def err_simple_logger_method(self):
        # pass
#
    # @lamda_logger()
    # def lamda_logger_method(self):
        # pass
#
    # @err_lambda_logger()
    # def err_lambda_logger_method(self):
        # pass


class TestLoggingDecorator(unittest.TestCase):
    """
    Test for logging decorator.
    """
    @staticmethod
    def _func_test(param1):
        pass

    def test_simple_logger(self):
        """
        Test simple_logger.
        """
        logger = LoggingTestMethod.logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            LoggingTestMethod().simple_logger_method()
        self.assertEqual(cm.output, [
            'DEBUG:{}:Start message'.format(logger.name),
            'DEBUG:{}:End message'.format(logger.name)
        ])

