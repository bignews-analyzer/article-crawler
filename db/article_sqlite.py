import logging

from db.default_sqlite import SqliteHelper
from db.static_sqlite import *


class ArticleSqliteHelper(SqliteHelper):
    def __init__(self,
                 logger: logging.Logger,
                 path: str):
        super().__init__(logger, path)
        self._path = path
        self._logger.info(f'{self._path} database init')

    def create_database(self):
        self._create_database(SQL_ARTICLE_TABLE_CREATE)
        self._logger.debug(f'article table created')
