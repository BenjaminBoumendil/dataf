#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Arg parser
----------

"""

import inspect
import argparse

from docutils.core import publish_doctree


class ArgParser:
    """
    Parser for CLI creation.
    """
    def __init__(self, parser_options, commands):
        """
        :param dict parser_options: arguments for argparse.ArgumentParser.
        :param dict commands: dict of all commands as key: command name, value: callable.
        """
        self.parser = argparse.ArgumentParser(**parser_options)
        self.commands = commands
        sub_parsers = self.parser.add_subparsers()

        for name, exec in sorted(self.commands.items()):
            if inspect.isclass(exec):
                exec = exec.run
            func_docstring = inspect.getdoc(exec)
            sub_pars = sub_parsers.add_parser(
                name, help=self._docstring_desc(func_docstring)
            )
            sub_pars.set_defaults(command=exec)
            func_signature = inspect.signature(exec)
            docstring_args = self._docstring_args(func_docstring)
            if hasattr(exec, 'setup_sub_pars'):
                exec.setup_sub_pars(sub_pars, func_signature, docstring_args)
            else:
                self._setup_sub_pars(sub_pars, func_signature, docstring_args)

    @staticmethod
    def _docstring_desc(docstring):
        """
        Parse docstring to get the first line of description.

        :param str docstring: docstring to parse.
        :returns: string of description
        """
        if docstring:
            return next(filter(''.__ne__, docstring.split('\n'))).strip()
        return ''

    @staticmethod
    def _docstring_args(docstring):
        """
        Parse docstring to get all args and attached docstring.

        :param str docstring: docstring to parse.
        :return: dict of args as key: arg name, value: arg description.
        """
        if docstring is None:
            return {}

        doctree = publish_doctree(docstring).asdom()
        fields = doctree.getElementsByTagName('field')

        kwargs_dict = {}
        for field in fields:
            field_name = field.getElementsByTagName('field_name')[0]
            field_body = field.getElementsByTagName('field_body')[0]
            kwargs_dict[field_name.firstChild.nodeValue.split()[-1]] = " ".join(
                c.firstChild.nodeValue for c in field_body.childNodes
            )

        return kwargs_dict

    @staticmethod
    def _setup_sub_pars(sub_pars, signature, docstring):
        """
        Setup one sub parser.

        :param obj sub_pars: sub parser to setup.
        :param obj signature: func signature.
        :param obj docstring: func docstring.
        """
        for param in filter('self'.__ne__, signature.parameters):
            sub_pars_arg = {'metavar': param, 'help': docstring.get(param, '')}
            if signature.parameters[param].default is not inspect._empty:
                arg_name = '--{}'.format(param)
                sub_pars_arg['default'] = signature.parameters[param].default
            else:
                arg_name = param
                if signature.parameters[param].annotation is not inspect._empty:
                    sub_pars_arg['choices'] = signature.parameters[param].annotation
                    sub_pars_arg['help'] = docstring.get(param, '') + " (choices: %(choices)s)"
            sub_pars.add_argument(arg_name, **sub_pars_arg)

    def parse(self):
        """
        Parse command argument.
        """
        args = self.parser.parse_args()
        if hasattr(args, 'command'):
            command_args = dict(filter(
                lambda x: x[0] != 'command', args.__dict__.items()
            ))
            if inspect.isclass(args.command):
                args.command().run(**command_args)
            else:
                args.command(**command_args)
        else:
            self.parser.print_help()
