from rest_framework.permissions import BasePermission


class AllowUnauthenticatedOnly(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdministratorUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsManagerUser(BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
