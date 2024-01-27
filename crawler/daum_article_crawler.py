import logging
import time
import typing

from datetime import date, timedelta

import selenium.webdriver.remote.webelement
from selenium.webdriver.common.by import By

from crawler.default_crawler import DefaultCrawler
from db.article_sqlite import ArticleSqliteHelper


class DaumArticleCrawler(DefaultCrawler):
    def __init__(self,
                 logger: logging.Logger,
                 db_helper: ArticleSqliteHelper,
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
        self.__db_helper = db_helper
        self.__article_data_batch = []
        self.__batch_limit = 150
        self.__total_count = 0
        self._base_url = 'https://news.daum.net/breakingnews/politics'
        self._logger.debug(f'crawler init')

    def __check_batch_insert(self):
        if len(self.__article_data_batch) >= self.__batch_limit:
            try:
                self.__db_helper.insert_values(self.__article_data_batch)
                self.__article_data_batch.clear()
            except:
                self._logger.exception('db insert data error occurred')

    def __get_article(self, news_link: str):
        self._logger.debug(f'article parsing start {news_link}')
        self._driver.get(news_link)

        company_name = self._driver.find_element(By.CSS_SELECTOR, '#kakaoServiceLogo').text

        content = ''
        for p in self._driver.find_elements(By.CSS_SELECTOR, '.article_view > section > p'):
            content += p.text
        self._logger.debug(f'get content finish\tlength: {len(content)}\tcompany: {company_name}\tlink: {news_link}')

        self.__article_data_batch.append((None, company_name, content, news_link))
        self.__check_batch_insert()
        self.__total_count += 1
        self._logger.debug(f'article parsing finish\ttotal: {self.__total_count}\tbatch size: {len(self.__article_data_batch)}')

    def __loop_day(self, date_str: str):
        page = 1
        max_page = 480
        while True:
            try:
                url = self._base_url + f'?page={page}&regDate={date_str}'
                self._driver.get(url)
                time.sleep(0.05)

                try:
                    self._driver.find_element(By.CSS_SELECTOR, '.btn_page.btn_next')
                except:
                    max_page = max(map(lambda x: int(x.text), self._driver.find_elements(By.CLASS_NAME, 'num_page')))

                self._logger.debug(f'date: {date_str}\tpage: {page}\t{url} loaded')

                news_items = self._driver.find_elements(By.CSS_SELECTOR, '.list_news2 > li')
                news_links = []
                for item in news_items:
                    news_links.append(item.find_element(By.CSS_SELECTOR, '.tit_thumb > .link_txt').get_attribute("href"))
                self._logger.debug(f'news items count: {len(news_links)}')

                for idx, link in enumerate(news_links):
                    try:
                        self.__get_article(link)
                    except:
                        self._logger.exception(f'date: {date_str}\tpage: {page}\tnum: {idx} load article error occurred')
            except:
                self._logger.exception(f'date: {date_str}\tpage: {page} error occurred')

            page += 3
            if page > max_page:
                self._logger.debug(f'date: {date_str}\tpage: {page} finish')
                break

    def start(self):
        self._logger.debug('crawling start')

        while self.__date <= self.__end_date:
            current_date_str = self.__date.strftime('%Y%m%d')
            self._logger.debug(f'now date: {self.__date.strftime("%Y-%m-%d")}')

            self.__loop_day(current_date_str)

            self.__date += timedelta(days=1)
        self._logger.debug('check batch empty')
        self.__check_batch_insert()
        self._logger.debug('crawling end')

    def close(self):
        super().close()
        self.__db_helper.close()
