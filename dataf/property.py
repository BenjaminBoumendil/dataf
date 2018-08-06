#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

property
--------

Custom Property decorator.

"""

from functools import wraps


class ClassProperty(property):
    """
    Decorator to set a property as classmethod.

    usage: @classproperty.
    """
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class StaticProperty(property):
    """
    Decorator to set a property as staticmethod.

    usage: @staticmethod.
    """
    def __get__(self, cls, owner):
        return self.fget.__get__(owner)()


def staticproperty(func):
    @wraps(func)
    @StaticProperty
    @staticmethod
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper


def classproperty(func):
    @wraps(func)
    @ClassProperty
    @classmethod
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper
