from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from app.contrib.permissions import UsersPermissions, PostPermissions
from app.service_layer.serializers import MyTokenObtainPairSerializer
from app.service_layer.service import RequestHandler
from app.consts import Methods
from app import swagger


class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(GenericViewSet, RetrieveModelMixin,
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

    @swagger_auto_schema(
        responses=swagger.user_get_by_id_doc['response'],
    )
    def retrieve(self, request, *args, **kwargs):
        user = self.handler.get_user(
            _id=kwargs.get('pk'), user_anonymous=request.user.is_anonymous
        )

        return Response(user, status=HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=swagger.user_list_doc['params'],
        responses=swagger.user_list_doc['response'],
    )
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
    http_method_names = [
        Methods.GET.value,
        Methods.PATCH.value,
        Methods.PUT.value,
        Methods.POST.value
    ]

    def __init__(self, **kwargs):
        self.handler = RequestHandler()
        super().__init__(**kwargs)

    @swagger_auto_schema(
        responses=swagger.post_get_by_id_doc['response'],
    )
    def retrieve(self, request, *args, **kwargs):
        post = self.handler.get_post(
            _id=kwargs.get('pk'),
            user_anonymous=request.user.is_anonymous
        )

        return Response(post, status=HTTP_200_OK)

    @swagger_auto_schema(
        request_body=swagger.post_create_doc['scheme'],
        responses=swagger.post_create_doc['response'],
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        response = self.handler.create_post(
            author=self.request.user,
            data=data
        )

        return Response(response, status=HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=swagger.post_get_list_doc['params'],
        responses=swagger.post_get_list_doc['response'],
    )
    def list(self, request, *args, **kwargs):
        """
        Query params *page
        """
        page = self.request.query_params.get('page', 1)
        posts = self.handler.get_list_posts(
            page=page, user_anonymous=request.user.is_anonymous
        )

        return Response(posts, status=HTTP_200_OK)

    @swagger_auto_schema(
        responses=swagger.like_post['response'],
    )
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        data = self.handler.add_like(user=request.user, pk_post=pk)

        return Response(data, status=HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=swagger.like_detail_post['params'],
        responses=swagger.like_detail_post['response'],
    )
    @action(detail=True, methods=['get'])
    def detail_like(self, request, pk=None):
        """
        Query params *date_from *date_to *page
        """
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        page = self.request.query_params.get('page', 1)

        data = self.handler.get_detail_likes(
            pk_post=pk,
            page=page,
            date_from=date_from,
            date_to=date_to,
        )

        return Response(data, status=HTTP_200_OK)
