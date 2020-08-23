from rest_framework.exceptions import ParseError


def _response_err(msg):
    # TODO add logs and status code
    return ParseError(msg)

