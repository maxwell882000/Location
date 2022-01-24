from rest_framework import permissions


class CheckPhone(permissions.BasePermission):
    message = 4444

    def has_permission(self, request, view):
        if request.user.is_phone_validated:
            return True
        request.user.phone_validation.save()
        return False


phone_permission = [permissions.IsAuthenticated, CheckPhone]
