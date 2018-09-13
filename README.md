# DataF

[![Documentation Status](https://readthedocs.org/projects/dataf/badge/?version=latest)](https://dataf.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/BenjaminBoumendil/dataf.svg?branch=master)](https://travis-ci.org/BenjaminBoumendil/dataf) [![codecov](https://codecov.io/gh/BenjaminBoumendil/dataf/branch/master/graph/badge.svg)](https://codecov.io/gh/BenjaminBoumendil/dataf)


DataF is a framework to create data oriented project in a fast way.

- Data and database manipulation using SQLAlchemy.
- Creating Web application using Flask.
- Creating CLI.
- Clean settings using Yaml.
- Logging.


Dependencies:
- python >= 3.5
- SQLAlchemy
- PyYAML
- slackclient
- flask
- flasgger
- docutils
- mako


Quick install:

    pip install dataf


Create project:

    dataf create_project name


Install without pip:

    git clone https://github.com/BenjaminBoumendil/dataf.git

    make

    pip install dataf/dist/dataf-x.x.x.tar.gz
