#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Test arg parser
---------------

Test suite for arg_parser.

"""

import unittest
import argparse

from dataf import ArgParser


class TestArgParser(unittest.TestCase):
    """
    Test for ArgParser class.
    """
    @classmethod
    def setUpClass(cls):
        cls.arg_parser = cls._create_arg_parser()

    @staticmethod
    def _test_command():
        """
        Test command.
        """
        pass

    @classmethod
    def _create_arg_parser(cls, opt=None, commands=None):
        """
        Create an ArgParser.

        :param dict opt: options for ArgParser.
        :param dict commands: commands for ArgParser.
        """
        opt = opt or {'description': 'Test'}
        commands = commands or {'test': cls._test_command}
        arg_parser = ArgParser(opt, commands)
        return arg_parser

    def test_init_create_arg_parser(self):
        """
        Test __init__ method create and ArgParser instance.
        """
        self.assertIsInstance(self.arg_parser, ArgParser)

    def test_init_create_argument_parser(self):
        """
        Test __init__ method create and ArgumentParser instance.
        """
        self.assertIsInstance(self.arg_parser.parser, argparse.ArgumentParser)

    def test_init_set_description(self):
        """
        Test __init__ method set parser description.
        """
        self.assertEqual(self.arg_parser.parser.description, 'Test')

    def test_init_set_commands(self):
        """
        Test __init__ method set commands.
        """
        test_cmd = next(filter(
            lambda x: getattr(x, '_name_parser_map', None) is not None,
            self.arg_parser.parser._actions
        ))
        self.assertIn('test', test_cmd.choices.keys())

    def test_docstring_args(self):
        """
        Test _docstring_args return dict with docstring param as ReStructuredText.
        """
        args = ArgParser._docstring_args(
            """
            Test docstring.

            :param str test: test string.
            :param str test2: second test string.
            """
        )
        self.assertEqual(
            {'test': 'test string.', 'test2': 'second test string.'}, args
        )

    def test_docstring_args_with_empty_string(self):
        """
        Test _docstring_args with an empty docstring.
        """
        args = ArgParser._docstring_args("")
        self.assertEqual({}, args)

    def test_docstring_args_with_none(self):
        """
        Test _docstring_args with None (no docstring in function).
        """
        args = ArgParser._docstring_args(None)
        self.assertEqual({}, args)

    def test_docstring_desc(self):
        """
        Test _docstring_desc return first line of docstring.
        """
        description = ArgParser._docstring_desc(
            """
            Test docstring.
            Second line.

            :param str test: test string.
            :param str test2: second test string.
            """
        )
        self.assertEqual('Test docstring.', description)

    def test_docstring_desc_with_empty_string(self):
        """
        Test _docstring_desc with an empty docstring.
        """
        description = ArgParser._docstring_desc('')
        self.assertEqual('', description)

    def test_docstring_desc_with_none(self):
        """
        Test _docstring_desc with None.
        """
        description = ArgParser._docstring_desc(None)
        self.assertEqual('', description)
