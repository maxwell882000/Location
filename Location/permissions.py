from rest_framework import permissions


class CheckPhone(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_phone_validated
