import argparse
import os
import typing
import threading

from datetime import datetime

import logger.default_logger
from logger.default_logger import Logger
from db.article_sqlite import ArticleSqliteHelper

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
    start_year, end_year = int(args.start_day[0:4]), int(args.end_day[0:4])
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
                         logger_file_path: str,
                         db_file_path: str,
                         year_interval: typing.Tuple[int, int]):
    logger_name = f'{year_interval[0]}_{year_interval[1]}'
    logger_file_name = f'{logger_name}_crawler.log'
    logger = init_logger(args, logger_name, 'debug', logger_file_path, logger_file_name).get_logger()
    logger.debug(f'{idx} logger init')

    db_file_name = f'{logger_name}_db.db'
    if not os.path.isdir(db_file_path):
        os.makedirs(db_file_path)
    db = ArticleSqliteHelper(logger, os.path.join(db_file_path, db_file_name))

    try:
        logger.debug(f'{idx} thread init')

        daum_crawler = DaumArticleCrawler(logger, db, year_interval[0], year_interval[1])
        daum_crawler.start()
        daum_crawler.close()
        logger.debug(f'{idx} thread finish')
    except:
        logger.exception(f'{idx} thread error occurred')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_print', type=int, help='로그 콘솔 출력 여부 true=1, false=0', default=0)
    parser.add_argument('--start_day', type=str, help='크롤링 시작일 yyyymmdd', default='20101001')
    parser.add_argument('--end_day', type=str, help='크롤링 마감일 yyyymmdd', default='20231231')
    parser.add_argument('--split', type=int, help='크롤러 스레드 개수', default=1)
    args = parser.parse_args()

    now_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    logger_file_path = f'./logs/{now_str}'
    db_file_path = f'./logs/{now_str}'

    main_logger = init_logger(args, 'main_logger', 'debug', logger_file_path, '0_main.log').get_logger()
    main_logger.debug('main logger init')

    try:
        intervals = find_interval(args)
        main_logger.debug(f'interval count: {len(intervals)}\tinterval: {intervals}')

        threads = []
        main_logger.debug('threads init')
        for idx, i in enumerate(intervals):
            thread = threading.Thread(target=start_crawler_thread, args=(idx, logger_file_path, db_file_path, i))
            thread.start()
            main_logger.debug(f'{idx} thread start')
            threads.append(thread)

        for thread in threads:
            thread.join()
    except:
        if main_logger is not None:
            main_logger.exception('critical error occurred')
