from rest_framework import permissions


class IsAdminorMe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.path == '/api/v1/users/me/':
                return True
            return bool(request.user.is_staff or request.user.role == 'admin')
