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

    def create_post(self, ):
        pass