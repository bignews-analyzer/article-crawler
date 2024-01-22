import logging

from crawler.default_crawler import DefaultCrawler


class DaumArticleCrawler(DefaultCrawler):
    def __init__(self,
                 logger: logging.Logger,
                 port: int = 4444,
                 container_name: str = '',
                 open_window: bool = True,
                 proxy: str = None):
        super().__init__(logger, port, container_name, open_window, proxy)
