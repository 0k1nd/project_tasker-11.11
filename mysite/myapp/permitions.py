
from rest_framework import permissions

class IsEditor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='editor').exists()