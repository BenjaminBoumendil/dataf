#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Base entity
-----------

Basic Entity as declarative to inherite from.

"""

from sqlalchemy import Column, Integer, Text, Index
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from dataf import ABCEntity, classproperty


@as_declarative()
class EmptyEntity(ABCEntity):
    """
    Entity without any fields.
    """
    @declared_attr
    def __tablename__(cls):
        """
        Set __tablename__ attr to lower case classe name.
        """
        return cls.__name__.lower()


@as_declarative()
class BaseEntity(ABCEntity):
    """
    Base entity with a primary key as integer.
    """
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        """
        Set __tablename__ attr to lower case classe name.
        """
        return cls.__name__.lower()


class DynamicEntity(ABCEntity):
    """
    Entity to create table on the fly.
    """
    __table__ = None

    @classmethod
    def create_index(cls, index_name, *cols, **kwargs):
        """
        Create an index object.

        :param str index_name: index name.
        :param obj cols: column objects to index.
        :return: Index object.
        """
        return Index(
            'ix_{}_{}_{}'.format(cls.schema, cls.name, index_name),
            *cols,
            **kwargs
        )

    @staticmethod
    def get_entity(name):
        """
        Get dynamic entity by name.

        :param str name: entity name.
        :return: classe entity.
        """
        return next(filter(
            lambda x: x.name.lower() == name, DynamicEntity.__subclasses__()
        ))

    @classproperty
    def name(cls):
        """
        Set name attr to lower case classe name.
        """
        return cls.__name__.lower()

    @classproperty
    def table(cls):
        """
        Get table object.

        :return: table object.
        """
        return cls.__table__

    @classmethod
    def table_from_db(cls, db):
        """
        Get table object from existing table in a database.

        :param obj db: DatabaseManager.
        :return: table object.
        """
        cls.__table__ = db.create_table_obj(cls.name, schema=cls.schema)
        return cls.__table__

    @classmethod
    def table_from_csv(cls, db, file, *, default_type=Text):
        """
        Create a table from a csv.

        :param obj db: DatabaseManager.
        :param obj file: opened file.
        :param obj default_type: columns default type if not filled, default: Text.
        :return: table object.
        """
        cols = map(
            lambda x: x.strip('"'), file.readline().strip('\n').split(';')
        )
        file.seek(0)
        return cls.table_from_lst(db, cols, default_type=default_type)

    @classmethod
    def table_from_lst(cls, db, cols, *, default_type=Text):
        """
        Create a table from a list of columns.

        :param obj db: DatabaseManager.
        :param list cols: list of column, elements can be string with col name
            or tuple with (col_name, type).
        :param obj default_type: columns default type if not filled, default: Text.
        :return: table object.
        """
        cls.__table__ = db.create_table_obj(
            cls.name, schema=cls.schema, autoload=False
        )
        for col in cols:
            if isinstance(col, tuple):
                cls.__table__.append_column(Column(*col))
            else:
                cls.__table__.append_column(Column(col, default_type))
        return cls.__table__

    @classmethod
    def create_mapper(cls, **kwargs):
        """
        Create a mapper if it does not exist.
        """
        try:
            mapper(cls, cls.__table__, **kwargs)
        except ArgumentError:
            pass
        return cls
