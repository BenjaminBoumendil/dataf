#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Test property
-------------

Test suite for property.

"""

from unittest import TestCase

from dataf import staticproperty, classproperty


class StaticPropertyTest:
    @staticproperty
    def static_property():
        return 'test_static_property'


class ClassPropertyTest:
    @classproperty
    def class_property(cls):
        return cls


class TestProperty(TestCase):
    """
    Test for property decorator.
    """
    def test_staticproperty_with_class(self):
        """
        Test for staticproperty decorator with class.
        """
        self.assertEqual(StaticPropertyTest.static_property, 'test_static_property')

    def test_staticproperty_with_instance(self):
        """
        Test for staticproperty decorator with instance.
        """
        self.assertEqual(StaticPropertyTest().static_property, 'test_static_property')

    def test_classproperty_with_class(self):
        """
        Test for classproperty decorator with class.
        """
        self.assertEqual(ClassPropertyTest.class_property, ClassPropertyTest)

    def test_classproperty_with_instance(self):
        """
        Test for classproperty decorator with instance.
        """
        self.assertEqual(ClassPropertyTest().class_property, ClassPropertyTest)
