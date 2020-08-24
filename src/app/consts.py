from enum import Enum


class Methods(Enum):
    PATCH = 'patch'
    POST = 'post'
    GET = 'get'
    DELETE = 'delete'
    PUT = 'put'


class LikeStatus(Enum):
    LIKE = 'Like'
    UNLIKE = 'UnLike'
