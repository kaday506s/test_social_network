from django.db import models

from django.conf import settings

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.core.paginator import Paginator


class MethodModels:

    @classmethod
    def _get_by_id(cls, model_orm, _id: int):
        return model_orm.objects.get(pk=_id)

    @classmethod
    def _get_pagination_list(cls, orm_objects, page: int):
        pagination_objs = Paginator(orm_objects, settings.PAGINATION_SIZE)
        return pagination_objs.page(page)


class Users(AbstractUser, MethodModels):
    """

    """
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True
    )

    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Middle name"),
    )

    mobile_phone = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name=_("Mobile phone"),
    )

    class Meta:
        verbose_name_plural = _('Users')
        verbose_name = _('User')

    def __str__(self):
        return self.username

    @classmethod
    def get_by_id(cls, _id: int):
        return cls._get_by_id(Users, _id)

    @classmethod
    def get_users_list(cls, page: int = 1):
        users = Users.objects.order_by('-id')
        return cls._get_pagination_list(users, page=page)


# TODO add like , analysis, views ...
class Post(models.Model, MethodModels):
    """

    """
    title = models.CharField(
        unique=True,
        max_length=128,
    )
    author = models.ForeignKey(
        Users,
        models.CASCADE,
        blank=False,
        null=False,
    )
    date_publication = models.DateTimeField(
        default=timezone.now,
    )
    text = models.TextField()

    class Meta:
        verbose_name_plural = _('Posts')
        verbose_name = _('Post')

    def __str__(self):
        return f"{self.title} - {self.author}"

    @classmethod
    def get_by_id(cls, _id: int):
        return cls._get_by_id(Post, _id)

    @classmethod
    def get_posts_list(cls, page: int = 1):
        posts = Post.objects.order_by('-date_publication')
        return cls._get_pagination_list(posts, page=page)

    @classmethod
    def get_by(cls, **kwargs):
        return Post.objects.get(**kwargs)

    @classmethod
    def create_orm_object(cls, **kwargs):
        return Post.objects.create(**kwargs)
