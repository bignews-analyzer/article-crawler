import logging


class Logger:
    def __init__(self,
                 log_name: str,
                 formatter: str = None,
                 level: str = 'debug'):
        self.__logger = logging.getLogger(log_name)

        if level == 'debug':
            self.__logger.setLevel(logging.DEBUG)
        elif level == 'info':
            self.__logger.setLevel(logging.INFO)
        elif level == 'warn':
            self.__logger.setLevel(logging.WARNING)
        elif level == 'error':
            self.__logger.setLevel(logging.ERROR)
        elif level == 'critical':
            self.__logger.setLevel(logging.CRITICAL)

        self.__formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if formatter is not None:
            self.__formatter = logging.Formatter(formatter)

    def add_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(stream_handler)

    def add_file_handler(self,
                         handler_path: str):
        file_handler = logging.FileHandler(handler_path, encoding='utf-8')
        file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.__logger
