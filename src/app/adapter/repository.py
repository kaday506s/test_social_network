import abc

from typing import Optional

from app.domain import model as domain_models
from app import models as django_models


class BasicRepository:
    @abc.abstractmethod
    def get_user_by_id(self, _id: int) -> domain_models.User:
        """
        :param _id:
        :return: domain_models.User
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_post_by_id(self, _id: int) -> domain_models.Post:
        """
        :param _id:
        :return: domain_models.Post
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_users(self) -> Optional[domain_models.User]:
        """
        :return: Optional[domain_models.Users]
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_posts(self) -> Optional[domain_models.Post]:
        """
        :return: Optional[domain_models.Posts]
        """
        raise NotImplemented

    @abc.abstractmethod
    def create_post(self, title: str, author: django_models.Users, text: str)\
            -> domain_models.Post:
        """
        :param title:
        :param author:
        :param text:
        :return: domain_models.Post
        """
        raise NotImplemented

    @abc.abstractmethod
    def create_user(self, username: str, email: str, first_name: str = None,
                    last_name: str = None, middle_name: str = None,
                    mobile_phone: str = None)\
            -> domain_models.User:
        """
        :param username:
        :param email:
        :param first_name:
        :param last_name:
        :param middle_name:
        :param mobile_phone:
        :return: domain_models.User
        """
        raise NotImplemented

    @abc.abstractmethod
    def update_user_by_id(self, _id: int, first_name: str = None,
                          last_name: str = None, middle_name: str = None,
                          mobile_phone: str = None)\
            -> domain_models.User:
        """
        :param _id:
        :param first_name:
        :param last_name:
        :param middle_name:
        :param mobile_phone:
        :return: domain_models.User
        """
        raise NotImplemented

    @abc.abstractmethod
    def update_post_by_id(self, _id: int, )\
            -> domain_models.Post:
        """
        :param _id:
        :return: domain_models.Post
        """
        raise NotImplemented

    @abc.abstractmethod
    def delete_user_by_id(self, _id: int):
        raise NotImplemented

    @abc.abstractmethod
    def delete_post_by_id(self, _id: int, user: django_models.Users):
        raise NotImplemented


class DjangoRepository(BasicRepository):
    orm_map = {
        domain_models.User: django_models.Users,
        domain_models.Post: django_models.Post,
    }

    def _to_domain_user(self, orm_obj):
        return domain_models.User(
            id=orm_obj.id,
            username=orm_obj.username,
            email=orm_obj.email,

            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            middle_name=orm_obj.middle_name,
            mobile_phone=orm_obj.mobile_phone,
        )

    def _to_domain_post(self, orm_obj):
        return domain_models.Post(
            id=orm_obj.id,
            title=orm_obj.title,
            author=orm_obj.author,

            text=orm_obj.text,
            date_publication=orm_obj.date_publication,
        )

    def _to_domain_obj(self, orm_obj):
        """

        """
        mapper = {
            django_models.Post: self._to_domain_post,
            django_models.Users: self._to_domain_user,
        }

        func = mapper.get(type(orm_obj))
        if func is None:
            raise Exception(
                f'there is no domain model for {type(orm_obj)}'
            )
        return func(orm_obj)

    def _get_by_id(self, django_model, _id: int):
        orm_obj = django_model.objects.get(pk=_id)
        return self._to_domain_obj(orm_obj)

    def get_user_by_id(self, _id: int) -> domain_models.User:
        return self._get_by_id(django_models.Users, _id=_id)

    def get_post_by_id(self, _id: int) -> domain_models.Post:
        return self._get_by_id(django_models.Post, _id=_id)

    def delete_post_by_id(self, _id: int, user: django_models.Users):
        try:
            obj_delete = django_models.Post.objects.get(
                author=user,
                pk=_id
            )
        except django_models.Post.objects.DoesNotExist:
            # TODO change
            raise Exception(
                f'does nt have ob'
            )
        obj_delete.delete()

    def _update_by_id(self, domain_class, _id: int, **kwargs):
        orm_model = self.orm_map.get(domain_class)

        orm_obj = orm_model.objects.get(id=_id)
        for key in kwargs.keys():
            if key not in domain_class.__dataclass_fields__.keys():
                raise Exception(
                    f"can not update field {key}, it does not exists"
                )
        for name, value in kwargs.items():
            setattr(orm_obj, name, value)
        orm_obj.save()

    def _get_orm_class(self, domain_obj):

        return self.orm_map.get(type(domain_obj))

    def _to_orm_obj(self, domain_obj):
        orm_class = self._get_orm_class(domain_obj)

        if orm_class is None:
            raise Exception(f'Unknown class {type(domain_obj)}')

        return orm_class.objects.get(id=domain_obj.id)

    def _get(self):
        pass