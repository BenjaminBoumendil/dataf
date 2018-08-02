Your first project
==================


Autogenerate project
--------------------


To create a project you can run the following command::

    $ dataf create_project <name>

This will create a directory <name> where you execute the command with a file <name>.py as an entry point for your application and a settings directory containing a settings.py file and bunch of yaml file to describe your settings.


Entry point
-----------

The entry point is made to avoid import problem, it contains:

- An init method initialising arg_parse_opt and commands for the arguments parser.

- A dev method for testing purpose, usefull if you want to test things to complex for the python CLI.

- A run method that launch the arguments parser.

You can add more command to your CLI just by adding entry in the commands dictionary, key is the command name and value is a function or a class with a run method.

For more information about the command parser and how to create more complex command see the ArgParser documentation in References or the How to sections.


Settings
--------

WIP
