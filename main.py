import argparse
import os
import typing

from datetime import datetime

import logger.default_logger
from logger.default_logger import Logger


def init_logger(args: argparse.Namespace,
                logger_name: str,
                logger_level: str,
                logger_file_path: str,
                logger_file_name: str) -> logger.default_logger.Logger:
    logger = Logger(log_name=logger_name, level=logger_level)

    if args.logger_print == 1:
        logger.add_stream_handler()

    # logger_file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.log'
    # logger_file_path = './logs'

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_print', type=int, help='로그 콘솔 출력 여부 true=1, false=0', default=0)
    parser.add_argument('--start_year', type=int, help='크롤링 시작 년도', default=2010)
    parser.add_argument('--end_year', type=int, help='크롤링 마감 년도', default=2023)
    parser.add_argument('--split', type=int, help='크롤러 스레드 개수', default=1)
    args = parser.parse_args()

    intervals = find_interval(args)
