from django.db import models

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
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


# TODO add like , analysis, views ...
class Post(models.Model):
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
