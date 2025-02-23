from logging import getLogger


class BaseService:
    def __init__(self):
        self.logger = self._logger()

    def _logger(self):
        return getLogger(self.__class__.__name__)

    def log_debug(self, message: str):
        self.logger.debug(message)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.error(message)
