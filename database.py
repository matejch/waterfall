"""
    This module contains the database connection and configuration.
"""
import sys
from typing import List

import aiosql

from dotenv import load_dotenv
import psycopg2 as psycopg2
from os import environ
import psycopg2.extras
from psycopg2.extras import execute_values

load_dotenv()


class Config:
    DATABASE_HOST = environ.get('DATABASE_HOST')
    DATABASE_USERNAME = environ.get('DATABASE_USERNAME')
    DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
    DATABASE_PORT = environ.get('DATABASE_PORT')
    DATABASE_NAME = environ.get('DATABASE_NAME')


class Database:
    """PostgreSQL Database class."""

    def __init__(self, config):
        self.host = config.DATABASE_HOST
        self.username = config.DATABASE_USERNAME
        self.password = config.DATABASE_PASSWORD
        self.port = config.DATABASE_PORT
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(host=self.host,
                                             user=self.username,
                                             password=self.password,
                                             port=self.port,
                                             dbname=self.dbname)
            except psycopg2.DatabaseError as e:
                print(e)
                sys.exit()
            finally:
                print('Connection opened successfully.')


db = Database(Config())
db.connect()

queries = aiosql.from_path("db/queries.sql", "psycopg2")


def store_contacts(contacts: List):
    try:
        queries.store_contacts(db.conn, contacts)
        db.conn.commit()
        print('Contacts stored successfully.')
    except Exception as e:
        print(e)
        db.conn.rollback()
        print('Store contacts FAILED.')
