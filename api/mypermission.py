from rest_framework import permissions


class IsStaffStatus(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff or request.user.is_superuser


class IsSuperUserStatus(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
