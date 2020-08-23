from rest_framework import permissions
from app.consts import Methods


class UsersPermissions(permissions.BasePermission):
    """
    Method for checking permissions
    """

    def has_permission(self, request, view, *args, **kwargs):
        if str(request.method).upper() == Methods.GET.value.upper():
            return True

        if request.user.is_anonymous:
            return False

        if request.user.is_superuser:
            return True

        if str(request.method).upper() == Methods.PATCH.value.upper():
            pk = view.kwargs.get('pk') \
                 or view.kwargs.get('user_pk')

            if request.user.pk == pk:
                return True

        return True


class PostPermissions(permissions.BasePermission):
    """
    Method for checking permissions
    """

    def has_permission(self, request, view, *args, **kwargs):

        if request.user.is_anonymous and \
                str(request.method).upper() == Methods.GET.value.upper():
            return True

        if request.user.is_anonymous:
            return False

        if request.user.is_superuser:
            return True

        # TODO think post permission
        if str(request.method).upper() == Methods.PATCH.value.upper():
            pk = view.kwargs.get('pk') \
                 or view.kwargs.get('user_pk')

            if request.user.pk == pk:
                return True
            else:
                return False

        return True
