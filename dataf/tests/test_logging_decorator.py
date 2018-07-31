#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Test logging decorator
----------------------

Test suite for logging_decorator.

"""

import logging
import unittest

from dataf import simple_logger, lambda_logger


class LoggingTestMethod:
    logger = logging.getLogger(__name__)

    @simple_logger('debug', start='Start', end='End')
    def simple_logger_method(self):
        pass

    @simple_logger('debug', err='Err', log_err=True)
    def err_simple_logger_method(self):
        raise Exception

    @simple_logger('debug', log_err=True)
    def err_simple_logger_method_without_msg(self):
        raise Exception

    @lambda_logger('debug',
        start=lambda p, cls: 'Start:{}:{}'.format(cls.__class__.__name__, p),
        end=lambda p, cls: 'End:{}:{}'.format(cls.__class__.__name__, p)
    )
    def lambda_logger_method(self, p):
        pass

    @lambda_logger('debug',
        err=lambda p, cls: 'Err:{}:{}'.format(cls.__class__.__name__, p),
        log_err=True
    )
    def err_lambda_logger_method(self, p):
        raise Exception

    @lambda_logger('debug', log_err=True)
    def err_lambda_logger_method_without_msg(self):
        raise Exception


class TestLoggingDecorator(unittest.TestCase):
    """
    Test for logging decorator.
    """
    @staticmethod
    def _func_test(param1):
        pass

    def test_simple_logger(self):
        """
        Test simple_logger start and end message.
        """
        logger = LoggingTestMethod.logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            LoggingTestMethod().simple_logger_method()
        self.assertEqual(cm.output, [
            'DEBUG:{}:Start'.format(logger.name),
            'DEBUG:{}:End'.format(logger.name)
        ])

    def test_simple_logger_with_error(self):
        """
        Test simple_logger with error.
        """
        logger = LoggingTestMethod.logger
        with self.assertLogs(logger=logger, level=logging.ERROR) as cm:
            with self.assertRaises(Exception):
                LoggingTestMethod().err_simple_logger_method()
        msg = 'ERROR:{}:Err\nTraceback'.format(logger.name)
        self.assertEqual(cm.output[0][:len(msg)], msg)

    def test_simple_logger_with_error_without_error_msg(self):
        """
        Test simple_logger with error but without error message.
        """
        logger = LoggingTestMethod.logger
        func = LoggingTestMethod().err_simple_logger_method_without_msg
        with self.assertLogs(logger=logger, level=logging.ERROR) as cm:
            with self.assertRaises(Exception):
                func()
        msg = 'ERROR:{}:{} error\nTraceback'.format(logger.name, func.__name__)
        self.assertEqual(cm.output[0][:len(msg)], msg)

    def test_lambda_logger(self):
        """
        Test lambda_logger start and end message.
        """
        logger = LoggingTestMethod.logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            LoggingTestMethod().lambda_logger_method('param')
        cls_name = LoggingTestMethod.__name__
        self.assertEqual(cm.output, [
            'DEBUG:{}:Start:{}:{}'.format(logger.name, cls_name, 'param'),
            'DEBUG:{}:End:{}:{}'.format(logger.name, cls_name, 'param')
        ])

    def test_lambda_logger_with_error(self):
        """
        Test lambda_logger with error.
        """
        logger = LoggingTestMethod.logger
        with self.assertLogs(logger=logger, level=logging.ERROR) as cm:
            with self.assertRaises(Exception):
                LoggingTestMethod().err_lambda_logger_method('param')
        msg = 'ERROR:{}:Err:{}:{}\nTraceback'.format(
            logger.name, LoggingTestMethod.__name__, 'param'
        )
        self.assertEqual(cm.output[0][:len(msg)], msg)

    def test_lambda_logger_with_error_without_error_msg(self):
        """
        Test lambda_logger with error but without error message.
        """
        logger = LoggingTestMethod.logger
        func = LoggingTestMethod().err_lambda_logger_method_without_msg
        with self.assertLogs(logger=logger, level=logging.ERROR) as cm:
            with self.assertRaises(Exception):
                func()
        msg = 'ERROR:{}:{} error\nTraceback'.format(logger.name, func.__name__)
        self.assertEqual(cm.output[0][:len(msg)], msg)
