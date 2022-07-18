from rest_framework import permissions
import ipdb

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        ipdb.set_trace()
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user.is_authenticated and obj == request.user)

class IsOwnerOrSuperUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (request.user.is_authenticated and obj == request.user or request.user.is_superuser)


class IsProviderOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
          request.user.is_authenticated
          and request.user.is_provider
        )


class IsProviderOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
          request.user.is_authenticated
          and request.user.is_provider == False
        )