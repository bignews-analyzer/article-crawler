import sqlite3
import logging


class SqliteHelper:
    def __init__(self,
                 logger: logging.Logger,
                 path: str):
        self._logger = logger
        self._conn = sqlite3.connect(path)
        self._logger.info(f'create database: {path}')
        self._conn.execute("PRAGMA encoding = 'UTF-16';")
        self._conn.execute("PRAGMA foreign_keys = ON;")

    def create_database(self,
                        create_query: str):
        cursor = self._conn.cursor()
        cursor.execute(create_query)

    def close_database(self):
        self._conn.close()
