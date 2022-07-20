from rest_framework import permissions
from users.models import User


class GetServiceOwnerOrAdmPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_superuser:
                return True

            if request.user == obj.contractor or request.user == obj.provider:
                return True

            return obj.is_active

        return request.user.is_superuser or obj.contractor == request.user


class IsProviderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_provider


class ListContractorServicesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        view_user = User.objects.get(id=view.kwargs["contractor_id"])

        return request.user.is_provider == False and request.user == view_user
