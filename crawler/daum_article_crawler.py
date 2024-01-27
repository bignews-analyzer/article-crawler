import logging
import time
import typing

from datetime import date, timedelta

import selenium.webdriver.remote.webelement

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
        self._base_url = 'https://news.daum.net/breakingnews/politics'
        self._logger.debug(f'crawler init')

    def __get_article(self, news_link: str):
        self._logger.debug(f'article parsing start {news_link}')
        self._driver.get(news_link)

        content = ''
        for p in self._driver.find_elements(By.CSS_SELECTOR, '.article_view > section > p'):
            content += p.text
        self._logger.debug(f'content length: {len(content)} get content finish')

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
        self._logger.debug('crawling end')

    def close(self):
        super().close()
