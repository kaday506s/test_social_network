from rest_framework.exceptions import ParseError

from app.contrib.logger import Logger

# TODO bad logger info
logger = Logger('response_err', './logs/').get_logger()


def _response_err(msg):
    logger.error(
        msg
    )
    return ParseError(msg)

