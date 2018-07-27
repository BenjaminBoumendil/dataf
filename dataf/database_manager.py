#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__doc__ = """

Database manager
----------------

Handle database basic operation using sqlalchemy.

Logs all error in exception object.
exception.logger: logger object.
exception.message: error message.

"""

import logging
from contextlib import contextmanager

from sqlalchemy import engine_from_config, MetaData, and_, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.sql import exists, text


class DatabaseManager:
    """
    Manage database interaction, Logs all error.
    """
    def __init__(self, configuration, prefix='', **kwargs):
        """
        Init logger and database connection, log and raise exception in case of
        connection error.

        :param dict configuration: engine configuration.
        :param str prefix: prefix to match and then strip from keys in
            ‘configuration’, default to ''.
        :param dict kwargs: each keyword argument overrides the corresponding
            item taken from the ‘configuration’ dictionary.
            Keyword arguments should not be prefixed
        """
        self.logger = logging.getLogger(__name__)
        try:
            self.database = engine_from_config(
                configuration, prefix=prefix, **kwargs
            )
            self._database_exists()
            self.Session = scoped_session(sessionmaker(self.database))
        except Exception as e:
            e.logger = self.logger
            e.message = 'Failed to connect to database'
            raise

    def _database_exists(self):
        """
        Check if database exists, raise exception if not.
        """
        connection = self.database.connect()
        connection.close()
        return True

    @contextmanager
    def session(self, *, raise_err=True, session_config=None):
        """
        Context manager for session, yield a session then commit,
        in case of error log exception and rollback session.

        :param bool raise_err: raise exception in case of error if True. Default to True.
        :param dict session_config: session configuration.
        """
        if session_config is None:
            session_config = {'autocommit': True, 'expire_on_commit': False}
        if self.Session.registry.has() is False:
            self.Session.configure(**session_config)
        session = self.Session()
        try:
            yield session
        except Exception as e:
            e.logger = self.logger
            e.message = 'Failed to commit'
            session.rollback()
            if raise_err is True:
                raise
        finally:
            session.close()

    def create_schema(self, name):
        """
        Create given schema, log and raise exception in case of error.

        :param str name: name of schema.
        """
        try:
            self.database.execute(CreateSchema(name))
        except Exception as e:
            e.logger = self.logger
            e.message = "Failed to create schema: {}".format(name)
            raise

    def drop_schema(self, name):
        """
        Drop given schema, log and raise exception in case of error.

        :param str name: name of schema.
        """
        try:
            self.database.execute(DropSchema(name))
        except Exception as e:
            e.logger = self.logger
            e.message = "Failed to drop schema: {}".format(name)
            raise

    def schema_exists(self, name):
        """
        Check if schema exists.

        :param str name: schema name.
        :return: True if exists otherwise False.
        """
        with self.session() as session:
            result = session.execute(text("""
                SELECT CASE
                WHEN EXISTS (SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name='{}')
                THEN true
                else false
                END
            """.format(name)))
        return result.scalar()

    def create_table_obj(self, name, *, schema=None, autoload=True):
        """
        Create an sqlalchemy table object.

        :param str name: name of table.
        :param str schema: table schema name. Default to None.
        :param bool autoload: autoload table structure. Default to True.
        """
        table = Table(
            name, MetaData(bind=self.database),
            autoload=autoload, schema=schema
        )

        return table

    def map_tables(self, tables, *, schema=None):
        """
        Map tables into python object, log and raise exception in case of error.

        :param list tables: list of tables name to map.
        :param str schema: table schema name. Default to None.
        :return: list of python object containing tables schemas.
        """
        try:
            metadata = MetaData(bind=self.database, schema=schema)
            metadata.reflect(only=tables)
            base = automap_base(metadata=metadata)
            base.prepare()
            return list(filter(
                lambda x: x.__table__.name in tables, base.classes
            ))
        except Exception as e:
            e.logger = self.logger
            e.message = "Failed to map table: {}".format(", ".join(tables))
            raise

    def add(self, entity):
        """
        Add one entity into current database, flush and expunge it.
        Raise and log exception in case of error.

        :param obj entity: Entity class with data to feed database.
        """
        with self.session() as session:
            session.add(entity)
            session.flush()
            session.expunge(entity)

    def add_all(self, entities):
        """
        Add list of entity into current database, flush and expunge it.
        Raise and log exception in case of error.

        :param list entities: List of entity class with data to feed.
        """
        with self.session() as session:
            session.add_all(entities)
            session.flush()
            session.expunge_all()

    def read(self, table):
        """
        Read all entry for one table, expunge and return it.
        Raise and log exception in case of error.

        :param obj table: Entity class with table schema.
        :return: list of database entry as entity class. None in case of error.
        """
        with self.session() as session:
            entities = session.query(table).all()
            session.expunge_all()
        return entities

    def delete(self, entity, merge=False):
        """
        Delete one entry, raise and log exception in case of error.

        :param obj entity: Entity instance to delete.
        """
        with self.session() as session:
            if merge is True:
                entity = session.merge(entity)
            session.delete(entity)
            session.flush()

    def update(self, entity, keys):
        """
        Update entity, select by id. Raise and log exception in case of error.

        :param obj entity: entity object to update.
        :paran list keys: list of keys to update.
        """
        update_dict = dict(filter(lambda x: x[0] in keys, entity.__dict__.items()))
        with self.session() as session:
            session.execute(
                entity.__table__.update().where(
                    entity.pk == getattr(entity, entity.pk.name)
                ).values(update_dict)
            )

    def entity_exists(self, filter):
        """
        Check if an entity exists on given filter, raise exception in case of error.

        :param obj entity: filter to apply to where clause.
        :return: True if exists otherwise False.
        """
        with self.session() as session:
            result = session.query(exists().where(and_(*filter))).scalar()
        return result

    def bulk_insert_mappings(self, obj, data):
        """
        Execute a bulk insert of data.

        :param obj obj: Class representing table schema.
        :param list data: list of dict representing data to add.
        """
        with self.session() as session:
            session.bulk_insert_mappings(obj, data)

    def bulk_save_objects(self, data, return_defaults=False):
        """
        Execute a bulk save of data.

        :param list data: list of table object with data to add.
        """
        with self.session() as session:
            session.bulk_save_objects(data, return_defaults=return_defaults)
