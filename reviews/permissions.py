from rest_framework import permissions
from services.models import Service


class IsInTheServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        service = Service.objects.get(id=view.kwargs["id_service"])

        return request.user == service.provider or request.user == service.contractor


class OwnerOrAdmPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_superuser or obj.user_critic == request.user
