import argparse
import os

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_print', type=int, help='로그 콘솔 출력 여부 true는 1/false는 0', default=0)
    args = parser.parse_args()
