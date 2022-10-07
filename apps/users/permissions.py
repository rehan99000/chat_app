from apps.utils.constants import USER_ROLES
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission check for admin role verification.
    """

    def has_permission(self, request, view):
        return request.user.role == USER_ROLES['ADMIN']

    def has_object_permission(self, request, view, obj):
        admins = getattr(obj, 'admins', getattr(getattr(obj, 'room'), 'admins'))
        if admins and request.user in admins.all():
            return True

        return super().has_object_permission(request, view, obj)


class IsCreator(permissions.BasePermission):
    """
    Permission check for user role verification.
    """
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user:
            return True

        return super().has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        return request.user.role == USER_ROLES['USER']
