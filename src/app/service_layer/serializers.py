import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BaseSerializer(serializers.Serializer,):
    # TODO think to better way
    def to_json_obj(self):
        """
        :return: 
        """""
        return json.loads(self.serialize())

    def serialize(self):
        """
        :return:
        """
        return JSONRenderer().render(self.data)


class UserSerializer(BaseSerializer):

    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    middle_name = serializers.CharField()

    mobile_phone = serializers.CharField()


class PostSerializer(BaseSerializer):

    title = serializers.CharField()
    author = UserSerializer()
    date_publication = serializers.DateTimeField()
    text = serializers.CharField()


# TODO -> -=+
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serialize Token
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
