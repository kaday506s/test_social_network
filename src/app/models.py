from django.db import models

from django.conf import settings

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator


class MethodModels:

    @classmethod
    def _get_by_id(cls, model_orm, _id: int):
        return model_orm.objects.get(pk=_id)

    @classmethod
    def _get_pagination_list(cls, orm_objects, page: int):
        pagination_objs = Paginator(orm_objects, settings.PAGINATION_SIZE)
        return pagination_objs.page(page)

    @classmethod
    def _get_content_type_model(cls, orm_model):
        obj_type = ContentType.objects.get_for_model(orm_model)
        return obj_type


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


class Like(models.Model, MethodModels):
    """

    """
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return f"{self.user.username}, {self.content_object}"

    @classmethod
    def add_like(cls, orm_post, user: Users):
        obj_type = cls._get_content_type_model(orm_post)

        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=orm_post.id, user=user
        )
        return like, is_created

    @classmethod
    def delete_like(cls, orm_post, user: Users):
        obj_type = ContentType.objects.get_for_model(orm_post)
        Like.objects.filter(
            content_type=obj_type, object_id=orm_post.id, user=user
        ).delete()


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

    likes = GenericRelation(Like)

    class Meta:
        verbose_name_plural = _('Posts')
        verbose_name = _('Post')

    def __str__(self):
        return f"{self.title} - {self.author}"

    def total_likes(self):
        return self.likes.count()

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

    @classmethod
    def get_detail_likes_users(cls, orm_post, page: int = 1, **kwargs):

        obj_type = cls._get_content_type_model(orm_post)
        users = Users.objects.filter(
            likes__content_type=obj_type, likes__object_id=orm_post.id,
            **kwargs
        ).order_by('-id')
        return cls._get_pagination_list(orm_objects=users, page=page)
