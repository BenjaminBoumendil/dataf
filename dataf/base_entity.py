#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Base entity
-----------

"""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from dataf import ABCEntity


@as_declarative()
class BaseEntity(ABCEntity):
    """
    Base entity with a primary key as integer.
    """
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        """
        Set __tablename__ attr to lower case class name.
        """
        return cls.__name__.lower()
