#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

${project_name.capitalize()}
${'-' * len(project_name)}

"""

from dataf import ArgParser


class ${project_name.capitalize()}:
    """
    ${project_name.capitalize()} entry points.
    """
    def __init__(self):
        self.commands = {
            'dev': self.dev,
        }
        self.arg_parse_opt = {
            'description': '${project_name.capitalize()} CLI.'
        }

    def dev(self):
        """
        Testing functions.
        """

    def run(self):
        """
        Parse arguments.
        """
        ArgParser(self.arg_parse_opt, self.commands).parse()


if __name__ == '__main__':
    ${project_name.capitalize()}().run()
