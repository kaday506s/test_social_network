import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


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
