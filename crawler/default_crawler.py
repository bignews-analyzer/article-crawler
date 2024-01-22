import logging

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

import platform


class DefaultCrawler:
    def __init__(self,
                 logger: logging.Logger,
                 port: int = 4444,
                 container_name: str = '',
                 open_window: bool = True,
                 proxy: str = None):
        self._logger = logger
        self.__open_chrome(open_window, container_name, port, proxy)

    def __open_chrome(self,
                      open_window: bool,
                      container_name: str,
                      port: int,
                      proxy: str):
        options = webdriver.ChromeOptions()

        if proxy is not None:
            self._logger.info(f'proxy enable - {proxy}')
            # proxy_extension = self.__connect_proxy(proxy)
            # options.add_extension(proxy_extension)
            # options.add_argument(f'--load-extension={os.path.join(os.getcwd(), "plugin")}')
            options.add_argument(f'--proxy-server={proxy}')

        if not open_window:
            options.add_argument('headless')
        # options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("lang=ko_KR")

        if platform.system() == 'Linux':
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            options.add_argument('user-agent=' + user_agent)

            self._logger.info('system os: Linux')
            self._driver = webdriver.Remote(
                f'http://selenium-hub:{port}/wd/hub',
                DesiredCapabilities.CHROME,
                options=options
            )
            self._logger.info('chrome connected')
        else:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            options.add_argument('user-agent=' + user_agent)

            self._logger.info('system os: others')
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self._logger.info('chrome connected')
        self._logger.info(f'connected chrome browser')

    def close(self):
        self._logger.info('chrome closed')
        self._driver.close()