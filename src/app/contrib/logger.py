import logging
from datetime import datetime


class Logger:

    def __init__(self, file_name: str, logs_path: str):
        self.file_name = file_name
        self.logs_path = logs_path
        self.logger = None

    def _init_logger(self) -> object:
        if not self.logger:
            self.logger = logging.getLogger(
                f"{self.file_name}"
            )

        return self.logger

    def _init_handler(self):
        file_handler = logging.FileHandler(
            f'{self.logs_path}{self.file_name}_'
            f'{"{:%Y-%m-%d}".format(datetime.now())}'
        )
        format_logs = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - \n%(message)s \n'
        )
        file_handler.setFormatter(format_logs)

        self.logger.addHandler(
            file_handler
        )

        return None

    def get_logger(self, ):
        self._init_logger()
        self._init_handler()

        self.logger.setLevel(logging.DEBUG)
        return self.logger
