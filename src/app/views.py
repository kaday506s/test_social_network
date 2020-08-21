
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from app.service_layer.serializers import MyTokenObtainPairSerializer
from app.service_layer.service import RequestHandler
from app.models import Users


class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):

    def __init__(self, **kwargs):
        self.handler = RequestHandler()
        super().__init__(**kwargs)

    def retrieve(self, request, *args, **kwargs):

        user = self.handler.get_user(_id=1)
        return Response(user, status=HTTP_200_OK)


class PostViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):

    def __init__(self, **kwargs):
        self.handler = RequestHandler()
        super().__init__(**kwargs)

    def retrieve(self, request, *args, **kwargs):
        post = self.handler.get_post(_id=kwargs.get('pk'))

        return Response(post, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        # TODO test local
        user = Users.objects.get(pk=1)

        response = self.handler.create_post(
            data.get('title'), data.get('text'), user
        )
        return Response(response, status=HTTP_201_CREATED)
