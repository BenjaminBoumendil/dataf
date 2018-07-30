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

    def test_parse_docstring(self):
        """
        Test _parse_docstring return dict with docstring param as ReStructuredText.
        """
        t = ArgParser._parse_docstring(
            """
            Test docstring.

            :param str test: test string.
            :param str test2: second test string.
            """
        )
        self.assertEqual(
            {'test': 'test string.', 'test2': 'second test string.'}, t
        )

    def test_parse_docstring_with_empty_string(self):
        """
        Test _parse_docstring with an empty docstring.
        """
        t = ArgParser._parse_docstring("")
        self.assertEqual({}, t)

    def test_parse_docstring_with_none(self):
        """
        Test _parse_docstring with None (no docstring in function).
        """
        t = ArgParser._parse_docstring(None)
        self.assertEqual({}, t)
