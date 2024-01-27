import logging
import typing

from db.default_sqlite import SqliteHelper
from db.static_sqlite import *


class ArticleSqliteHelper(SqliteHelper):
    def __init__(self,
                 logger: logging.Logger,
                 path: str):
        super().__init__(logger, path)
        self._path = path
        self._logger.info(f'{self._path} database init')
        self.__create_database()

    def __create_database(self):
        self._create_database(SQL_ARTICLE_TABLE_CREATE)
        self._logger.debug(f'article table created')

    def insert_values(self, values: typing.List[typing.Any]):
        self._conn.executemany('INSERT INTO article VALUES (?,?,?,?)', values)
        self._conn.commit()
        self._logger.debug(f'{len(values)} values inserted')

    def close(self):
        super()._close_database()
        self._logger.debug(f'{self._path} db closed')
