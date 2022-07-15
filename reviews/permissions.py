from rest_framework import permissions


class OwnerOrAdmPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_superuser or obj.user_critic == request.user
