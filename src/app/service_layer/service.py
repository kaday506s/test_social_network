from app.adapter.repository import DjangoRepository
from app.service_layer import serializers


class RequestHandler:
    repository_class = DjangoRepository

    def __init__(self, *args, **kwargs):
        self.repository = DjangoRepository()

    def get_user(self, _id: int):
        user = self.repository.get_user_by_id(_id=_id)
        serializer = serializers.UserSerializer(user)

        return serializer.to_json_obj()

    def get_post(self, _id: int):
        post = self.repository.get_post_by_id(_id=_id)
        serializer = serializers.PostSerializer(post)

        return serializer.to_json_obj()

    def create_post(self, title: str, text: str, author):
        post = self.repository.create_post(
            title=title, text=text, author=author
        )
        serializer = serializers.PostSerializer(post)

        return serializer.to_json_obj()
