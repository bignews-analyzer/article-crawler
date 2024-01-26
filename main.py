import argparse
import os
import typing
import threading

from datetime import datetime

import logger.default_logger
from logger.default_logger import Logger
from crawler.daum_article_crawler import DaumArticleCrawler


def init_logger(args: argparse.Namespace,
                logger_name: str,
                logger_level: str,
                logger_file_path: str,
                logger_file_name: str) -> logger.default_logger.Logger:
    logger = Logger(log_name=logger_name, level=logger_level)

    if args.logger_print == 1:
        logger.add_stream_handler()

    if not os.path.isdir(logger_file_path):
        os.makedirs(logger_file_path)

    logger_file_path = os.path.join(logger_file_path, logger_file_name)
    logger.add_file_handler(logger_file_path)

    return logger


def find_interval(args: argparse.Namespace) -> typing.List[typing.Tuple[int, int]]:
    start_year, end_year = int(args.start_year), int(args.end_year)
    split_count = int(args.split)

    total_length = end_year - start_year + 1
    base_length = total_length // split_count
    remainder = total_length % split_count

    intervals = []
    start = start_year

    for i in range(split_count):
        end = start + base_length + (1 if i < remainder else 0) - 1
        intervals.append((start, end))
        start = end + 1

    return intervals


def start_crawler_thread(idx: int,
                         logger: logger.default_logger.Logger,
                         year_interval: typing.Tuple[int, int]):
    logger = logger.get_logger()
    try:
        logger.debug(f'{idx} thread init')

        daum_crawler = DaumArticleCrawler(logger)
        for _ in range(1000000000): pass
        daum_crawler.close()
        logger.debug(f'{idx} thread finish')
    except:
        logger.exception(f'{idx} thread error occurred')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_print', type=int, help='로그 콘솔 출력 여부 true=1, false=0', default=0)
    parser.add_argument('--start_year', type=int, help='크롤링 시작 년도', default=2010)
    parser.add_argument('--end_year', type=int, help='크롤링 마감 년도', default=2023)
    parser.add_argument('--split', type=int, help='크롤러 스레드 개수', default=1)
    args = parser.parse_args()

    logger_file_path = f'./logs/{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
    main_logger = init_logger(args, 'main_logger', 'debug', logger_file_path, '0_main.log').get_logger()
    main_logger.debug('main logger init')

    try:
        intervals = find_interval(args)
        main_logger.debug(f'interval count: {len(intervals)}\tinterval: {intervals}')

        threads = []
        main_logger.debug('threads init')
        for idx, i in enumerate(intervals):
            logger_name = f'{i[0]}_{i[1]}'
            logger_file_name = f'{logger_name}_crawler.log'
            logger = init_logger(args, logger_name, 'debug', logger_file_path, logger_file_name)
            main_logger.debug(f'{idx} thread logger init')

            thread = threading.Thread(target=start_crawler_thread, args=(idx, logger, i))
            thread.start()
            main_logger.debug(f'{idx} thread start')
            threads.append(thread)

        for thread in threads:
            thread.join()
    except:
        if main_logger is not None:
            main_logger.exception('critical error occurred')
