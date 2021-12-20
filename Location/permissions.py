from rest_framework import permissions


class CheckPhone(permissions.BasePermission):
    code = 410
    def has_permission(self, request, view):
        return request.user.is_phone_validated
