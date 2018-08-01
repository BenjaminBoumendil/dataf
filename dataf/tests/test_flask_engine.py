#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Test flask engine
-----------------

Test suite for flask_engine.

"""

import unittest

from flask import Flask
from flask.views import MethodView
from flasgger import Swagger

from dataf import FlaskEngine


class TestView(MethodView): pass


# SWAGGER = {
#     'template': {
#         'info': {
#             'title': 'Sirene API',
#             'contact': {'Slack': 'lbc-hrm-dev'}
#         },
#         'host': 'localhost:5000'
#     },
#     'config': {
#         'headers': [],
#         'specs': [{
#             'endpoint': 'apispec_1',
#             'route': '/apispec_1.json',
#             'rule_filter': lambda x: True ,
#             'model_filter': lambda x: True,
#         }],
#         'static_url_path': '/flasgger_static',
#         'swagger_ui': True,
#         'specs_route': '/api/docs/',
#     }
# }


class TestFlaskEngine(unittest.TestCase):
    """
    Test suite for FlaskEngine class.
    """
    def test_init(self):
        """
        Test __init__ method.
        """
        instance = FlaskEngine({'/test': {'cls': TestView}}, {})
        self.assertIsInstance(instance, FlaskEngine)
        self.assertIsInstance(instance.app, Flask)
        self.assertIsInstance(instance.swagger, Swagger)
