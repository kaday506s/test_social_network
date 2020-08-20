from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from app.service_layer.service import RequestHandler


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):

    def create(self, request, *args, **kwargs):
        # TODO
        return Response({'OK':'OK'})

    def retrieve(self, request, *args, **kwargs):
        user = RequestHandler().get_user(_id=1)
        return Response(user)


