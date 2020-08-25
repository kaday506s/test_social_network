import abc

from typing import Optional, Union, List

from app.contrib.response_err import _response_err
from app.domain import model as domain_models
from app.consts import LikeStatus
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
    def get_users(self, page: int) -> List[domain_models.User]:
        """
        :return: Optional[domain_models.Users]
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_posts(self, page: int) -> Optional[domain_models.Post]:
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

    # TODO append create user
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

    # TODO append delete user
    @abc.abstractmethod
    def delete_user_by_id(self, _id: int):
        raise NotImplemented

    @abc.abstractmethod
    def delete_post_by_id(self, _id: int, user: django_models.Users):
        raise NotImplemented

    @abc.abstractmethod
    def post_like(self, user: django_models.Users, pk_post: int):
        """
        :param user:
        :param pk_post:
        :return:
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_users_like_by_post(self, pk_post: int, page: int,
                               date_from: str = None, date_to: str = None):
        """
        :param date_to:
        :param date_from:
        :param pk_post:
        :param page:
        :return:
        """
        raise NotImplemented


class DjangoRepository(BasicRepository):
    """
        ORM models can change in future
    """
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
            likes=orm_obj.total_likes()
        )

    def _get_by_id_from_orm(self, django_model, _id: int) -> \
            Union[django_models.Users, django_models.Post]:
        """
            Get Django * model by id
        """
        try:
            orm_obj = django_model.get_by_id(_id=_id)

        except django_model.DoesNotExist:
            raise _response_err(f'{django_models} DoesNotExist')

        except AttributeError as err:
            raise _response_err(err)

        return orm_obj

    def get_user_by_id(self, _id: int) -> domain_models.User:
        orm_obj = self._get_by_id_from_orm(django_models.Users, _id=_id)

        return self._to_domain_obj(orm_obj)

    def get_post_by_id(self, _id: int) -> domain_models.Post:
        orm_obj = self._get_by_id_from_orm(django_models.Post, _id=_id)

        return self._to_domain_obj(orm_obj)

    def delete_post_by_id(self, _id: int, user: django_models.Users):
        try:
            obj_delete = django_models.Post.objects.get(
                author=user,
                pk=_id
            )
        except django_models.Post.DoesNotExist as err:
            raise _response_err(err)

        obj_delete.delete()

    def _update_by_id(self, domain_class, _id: int, **kwargs):
        django_model = self.orm_map.get(domain_class)
        orm_obj = self._get_by_id_from_orm(django_model, _id=_id)

        for key in kwargs.keys():
            if key not in domain_class.__dataclass_fields__.keys():
                raise _response_err(
                    f"Can not update field {key}"
                )

        for name, value in kwargs.items():
            setattr(orm_obj, name, value)

        orm_obj.save()

    def _get_orm_class(self, domain_obj):

        return self.orm_map.get(type(domain_obj))

    def _domain_to_orm_obj(self, domain_obj):
        orm_class = self._get_orm_class(domain_obj)

        if orm_class is None:
            raise _response_err(f'Unknown class {type(domain_obj)}')

        return orm_class.objects.get(id=domain_obj.id)

    # TODO -> to domain then model
    def create_post(self, title: str, text: str, author: django_models.Users) \
            -> domain_models.Post:

        try:
            django_models.Post.get_by(title=title, author=author)

        except django_models.Post.DoesNotExist:
            orm_obj = django_models.Post.create_orm_object(
                title=title,
                author=author,
                text=text
            )
            return self._to_domain_obj(orm_obj)

        raise _response_err(f"{title} already exists")

    def _to_domain_list(self, orm_objs) \
            -> List[Union[domain_models.User, domain_models.Post]]:

        domain_items = []
        for item in orm_objs:
            domain_items.append(self._to_domain_obj(item))

        return domain_items

    def _to_domain_obj(self, orm_obj):
        mapper = {
            django_models.Post: self._to_domain_post,
            django_models.Users: self._to_domain_user,
        }

        func = mapper.get(type(orm_obj))
        if func is None:
            raise _response_err(f'There is not domain model for {type(orm_obj)}')

        return func(orm_obj)

    def get_users(self, page: int) -> List[domain_models.User]:
        try:
            orm_objs = django_models.Users.get_users_list(page=page)

        # TODO change Exception
        except Exception as err:
            raise _response_err(err)

        return self._to_domain_list(orm_objs)

    def get_posts(self, page: int) -> List[domain_models.Post]:

        try:
            orm_objs = django_models.Post.get_posts_list(page=page)

        # TODO change Exception
        except Exception as err:
            raise _response_err(err)

        return self._to_domain_list(orm_objs)

    def post_like(self, user, pk_post):
        try:
            orm_post = django_models.Post.get_by_id(_id=pk_post)
        except django_models.Post.DoesNotExist:
            raise _response_err(f'Post - id {pk_post} DoesNotExist')

        like_orm, is_created = django_models.Like.add_like(
            orm_post=orm_post, user=user
        )
        if not is_created:
            django_models.Like.delete_like(
                orm_post=orm_post, user=user
            )
            return LikeStatus.UNLIKE.value

        return LikeStatus.LIKE.value

    def get_users_like_by_post(self, pk_post: int, page: int,
                               date_from: str = None, date_to: str = None):
        date_range = {}
        if date_from and date_to:
            date_range = {
                'likes__timestamp__gte': date_from,
                'likes__timestamp__lte': date_to
            }

        try:
            orm_post = django_models.Post.get_by_id(_id=pk_post)
        except django_models.Post.DoesNotExist:
            raise _response_err(f'Post - id {pk_post} DoesNotExist')
        try:
            users_like = django_models.Post.get_detail_likes_users(
                orm_post=orm_post, page=page, **date_range
            )
        except Exception as err:
            raise _response_err(err)
        return self._to_domain_list(users_like)
