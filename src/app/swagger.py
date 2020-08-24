from drf_yasg.openapi import (

    Parameter,
    IN_QUERY,
    TYPE_STRING,
    TYPE_INTEGER,

    TYPE_OBJECT,
    Schema
)
from app.service_layer.serializers import (
    PostSerializer,
    UserSerializer,
    PostLiteSerializer,
    UserLiteSerializer,
    LikeSerializer
)


user_list_doc = {
    'params': [
        Parameter('page', IN_QUERY, type=TYPE_INTEGER, required=False)
    ],
    'response': {
        "200": UserSerializer(many=True),
        "200_unAuth": UserLiteSerializer(many=True),
        "200_Data": "{'result': * Serializer *, 'page': 'NumPage'}",
    }
}
user_get_by_id_doc = {
    'response': {
        "200": PostSerializer(),
        "200_unAuth": UserLiteSerializer(),
    }
}

post_create_doc = {
    'scheme': Schema(
        type=TYPE_OBJECT,
        properties={
            'title': Schema(
                type=TYPE_STRING,
                description='Title of Post',
                default={},
            ),
            'text': Schema(
                type=TYPE_STRING,
                description='Text of Post',
                default={},
            ),
        },
        required=['action']
    ),
    'response': {
        "201": PostSerializer(),
    }
}

post_get_list_doc = {
    'params': [
        Parameter('page', IN_QUERY, type=TYPE_INTEGER, required=False)
    ],
    'response': {
        "200":  PostSerializer(many=True),
        "200_unAuth": PostLiteSerializer(many=True),
        "200_Data": "{'result': * Serializer *, 'page': 'NumPage'}",
    }
}
post_get_by_id_doc = {
    'response': {
        "200":  PostSerializer(),
        "200_unAuth": PostLiteSerializer(),
    }
}

like_post = {
    'response': {
        "200":  "{'id_post': pk_post, 'like_status': Like/UnLike}"
    }
}

like_detail_post = {
    'params': [
        Parameter(
            'page', IN_QUERY,
            type=TYPE_INTEGER,
            required=False
        ),
        Parameter(
            'date_from', IN_QUERY,
            type=TYPE_STRING,
            required=False,
            description="date filter"
        ),
        Parameter(
            'date_to', IN_QUERY,
            type=TYPE_STRING,
            required=False,
            description="date filter"
        ),
    ],
    'response': {
        "200":  LikeSerializer(many=True),
        "200_Data": "{'result': * Serializer *, 'page': 'NumPage'}",
    }
}