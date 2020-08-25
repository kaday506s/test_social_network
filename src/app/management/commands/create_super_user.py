from django.core.management.base import BaseCommand
from app.models import Users


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def create_user(self, username):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            user = Users.objects.create_superuser(
                username=username, password='1234',
                email='test@ts.ts'
            )

    def handle(self, *args, **kwargs):
        username = kwargs.get('username')
        self.create_user(username=username)
