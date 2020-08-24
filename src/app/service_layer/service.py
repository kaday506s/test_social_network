from app.adapter.repository import DjangoRepository
from app.service_layer import serializers


class RequestHandler:
    repository_class = DjangoRepository

    def __init__(self, *args, **kwargs):
        self.repository = DjangoRepository()

    def get_user(self, _id: int, user_anonymous: bool) -> dict:
        user = self.repository.get_user_by_id(_id=_id)

        if user_anonymous:
            serializer = serializers.UserLiteSerializer(user)
        else:
            serializer = serializers.UserSerializer(user)

        return serializer.to_json_obj()

    def get_list_users(self, page: int, user_anonymous: bool) -> dict:
        user = self.repository.get_users(page=page)

        if user_anonymous:
            serializer = serializers.UserLiteSerializer(user, many=True)
        else:
            serializer = serializers.UserSerializer(user, many=True)

        return {'results': serializer.data, 'page': page}

    def get_list_posts(self, page: int, user_anonymous: bool) -> dict:
        posts = self.repository.get_posts(page=page)

        if user_anonymous:
            serializer = serializers.PostLiteSerializer(posts, many=True)
        else:
            serializer = serializers.PostSerializer(posts, many=True)

        return {'results': serializer.data, 'page': page}

    def get_post(self, _id: int, user_anonymous: bool):
        post = self.repository.get_post_by_id(_id=_id)

        if user_anonymous:
            serializer = serializers.PostLiteSerializer(post)
        else:
            serializer = serializers.PostSerializer(post)

        return serializer.to_json_obj()

    def create_post(self, author, data: dict):

        post_data = serializers.PostSerializer(data=data)
        post_data.is_valid(raise_exception=True)

        post = self.repository.create_post(
            title=data.get('title'), text=data.get('text'), author=author
        )
        serializer = serializers.PostSerializer(post)

        return serializer.to_json_obj()

    def add_like(self, user, pk_post: int) -> dict:
        like_status = self.repository.post_like(user=user, pk_post=pk_post)

        return {'id_post': pk_post, 'like_status': like_status}

    def get_detail_likes(self, pk_post: int, page: int, date_from: str = None,
                         date_to: str = None) -> dict:

        users_like = self.repository.get_users_like_by_post(
            pk_post=pk_post, page=page, date_from=date_from, date_to=date_to
        )
        serializer = serializers.LikeSerializer(users_like, many=True)

        return {'results': serializer.data, 'page': page}
