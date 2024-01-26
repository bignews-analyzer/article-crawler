import logging
import time

from datetime import date, timedelta
from crawler.default_crawler import DefaultCrawler

from selenium.webdriver.common.by import By


class DaumArticleCrawler(DefaultCrawler):
    def __init__(self,
                 logger: logging.Logger,
                 start_year: int,
                 end_year: int,
                 port: int = 4444,
                 container_name: str = '',
                 open_window: bool = True,
                 proxy: str = None):
        super().__init__(logger, port, container_name, open_window, proxy)
        self.__page = 1
        self.__start_data = date(start_year, 1, 1)
        self.__end_date = date(end_year, 12, 31)
        self.__date = self.__start_data
        self._logger.debug(f'crawler init')
        self._base_url = 'https://news.daum.net/breakingnews/politics'

    def __loop_day(self, date_str: str):
        url = self._base_url + f'?page=1&regDate={date_str}'
        self._driver.get(url)
        self._logger.debug(f'{url} loaded')

        news_items = self._driver.find_elements(By.CSS_SELECTOR, '.list_news2 > li')
        self._logger.debug(f'news items: {len(news_items)}')

        time.sleep(5)

    def start(self):
        self._logger.debug('crawling start')

        while self.__date <= self.__end_date:
            current_date_str = self.__date.strftime('%Y%m%d')
            self._logger.debug(f'now date: {self.__date.strftime("%Y-%m-%d")}')

            self.__loop_day(current_date_str)

            self.__date += timedelta(days=1)
        self._logger.debug('crawling end')

    def close(self):
        super().close()
