How to
======


Create and customise your CLI
-----------------------------


Add commands
^^^^^^^^^^^^

Commands are generated from the 'commands' dictionary passed to ArgParse.

Just add entry to the dictonary as key: command name, value: command function or class.


With a function:

.. code-block:: python
    :linenos:
    :emphasize-lines: 3, 4, 5
    :caption: entry_point.py

    class EntryPoint:
        def __init__(self):
            self.commands = {
                'test': self.test_command
            }
            self.arg_parse_opt = {
                'description': 'Test CLI.'
            }

        def test_command(self):
            print('Hello World')

        def run(self):
            ArgParser(self.arg_parse_opt, self.commands).parse()


    if __name__ == '__main__':
        EntryPoint().run()

.. code-block:: console

    $ python entry_point.py test
    Hello World


With a class:

.. code-block:: python
    :linenos:
    :caption: entry_point.py

    class TestCommand:
        def run(self):
            print('Hello World')


    class EntryPoint:
        def __init__(self):
            self.commands = {
                'test': TestCommand
            }
            self.arg_parse_opt = {
                'description': 'Test CLI.'
            }

        def run(self):
            ArgParser(self.arg_parse_opt, self.commands).parse()


    if __name__ == '__main__':
        EntryPoint().run()

.. code-block:: console

    $ python entry_point.py test
    Hello World


Notice that we only pass the class in the commands dictionary, parser will instantiate and call the run method by itself, this is to avoid useless class instantiation.

.. TIP:: If you need to give parameters to your classe, one option is to use `partial`_.

.. _partial: https://docs.python.org/3.6/library/functools.html#functools.partial


Having arguments for a command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command arguments is generated from the function signature, function required parameters will result in command function parameters and function optional parameters in command optional parameters.

.. code-block:: python
    :linenos:

    def test_command(req_arg, opt_arg='default'):
        print('{} {}'.format(req_arg, opt_arg))

.. code-block:: console

    $ python entry_point.py test Hello
    Hello default

    $ python entry_point.py test Hello --opt_arg=World
    Hello World


Customise command helper
^^^^^^^^^^^^^^^^^^^^^^^^

Helper are generated from the function docstring, first line of docstring is for the command description and docstring param for the command arguments.

.. code-block:: python
    :linenos:

    def test_command(req_arg, opt_arg='default'):
        """
        Testing command.

        :param str req_arg: required argument.
        :param str opt_arg: optional argument.
        """
        print('{} {}'.format(req_arg, opt_arg))

.. code-block:: console

    $ python entry_point.py -h
    usage: entry_point.py [-h] {test} ...

    Test CLI.

    positional arguments:
      {test}
        test              Testing command.

    optional arguments:
      -h, --help         show this help message and exit

    $ python entry_point.py dev -h
    usage: entry_point.py dev [-h] [--opt_arg opt_arg] req_arg

    positional arguments:
      req_arg            required argument.

    optional arguments:
      -h, --help         show this help message and exit
      --opt_arg opt_arg  optional argument.


Define a list of choices for a command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can define a list of choices using annotation.

.. code-block:: python
    :linenos:

    def test_command(req_arg: ['foo', 'bar'], opt_arg='default'):
        """
        Testing command.

        :param str req_arg: required argument.
        :param str opt_arg: optional argument.
        """
        print('{} {}'.format(req_arg, opt_arg))

.. code-block:: console

    $ python entry_point.py dev -h
    usage: entry_point.py dev [-h] [--opt_arg opt_arg] req_arg

    positional arguments:
      req_arg            required argument. (choices: bar, foo)

    optional arguments:
      -h, --help         show this help message and exit
      --opt_arg opt_arg  optional argument.

.. TIP:: For big list choices consider using a variable.

    .. code-block:: python
        :linenos:

        _choices = ['arg' ...]
        def test_command(req_arg: _choices):
            pass


Override sub parser behavior for a command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To define a custom sub parser behavior you must use a classe and define a 'setup_sub_parser' function in it who take 3 arguments:

- sub_pars: subparser object from argparser, result of add_parser method from `add_subparsers`_.

- signature: function signature, result of `inspect.signature`_ method.

- docstring: docstring arguments as dict. key: arg name, value: arg description.

.. _add_subparsers: https://docs.python.org/3.6/library/argparse.html#sub-commands

.. _inspect.signature: https://docs.python.org/3.6/library/inspect.html#introspecting-callables-with-the-signature-object


Create and customise your settings with yaml
--------------------------------------------

WIP


Manipulating a database
-----------------------

WIP


Create a web app
----------------

WIP


Customise your logging
----------------------

WIP
