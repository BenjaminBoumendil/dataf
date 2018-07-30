#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

property
--------

Custom Property decorator.

"""

from functools import wraps


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class StaticProperty(property):
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