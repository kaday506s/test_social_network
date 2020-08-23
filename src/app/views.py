
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from app.contrib.permissions import UsersPermissions, PostPermissions
from app.service_layer.serializers import MyTokenObtainPairSerializer
from app.service_layer.service import RequestHandler
from app.consts import Methods


class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin,
                  ListModelMixin):

    permission_classes = (UsersPermissions,)
    http_method_names = [
        Methods.GET.value,
        Methods.PATCH.value,
        Methods.PUT.value
    ]

    def __init__(self, **kwargs):
        self.handler = RequestHandler()
        super().__init__(**kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = self.handler.get_user(
            _id=kwargs.get('pk'), user_anonymous=request.user.is_anonymous
        )

        return Response(user, status=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        Query params ?page=1 *
        """
        # TODO think to use pop and other kwargs -> filter
        page = self.request.query_params.get('page', 1)
        user = self.handler.get_list_users(
            page=page, user_anonymous=request.user.is_anonymous
        )

        return Response(user, status=HTTP_200_OK)


class PostViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    permission_classes = (PostPermissions,)

    def __init__(self, **kwargs):
        self.handler = RequestHandler()
        super().__init__(**kwargs)

    def retrieve(self, request, *args, **kwargs):
        post = self.handler.get_post(
            _id=kwargs.get('pk'),
            user_anonymous=request.user.is_anonymous
        )

        return Response(post, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        response = self.handler.create_post(
            author=self.request.user,
            data=data
        )

        return Response(response, status=HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        Query params page
        """
        # TODO think to use pop and other kwargs -> filter
        page = self.request.query_params.get('page', 1)

        posts = self.handler.get_list_posts(
            page=page, user_anonymous=request.user.is_anonymous
        )

        return Response(posts, status=HTTP_200_OK)
