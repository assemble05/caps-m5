from rest_framework import permissions

class OwnerOrAdmPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_superuser:
                return True
            
            if request.user.is_provider:
                return obj.is_active

            if request.user == obj.contractor:
                return obj.is_delete == False
            
        return request.user.is_superuser or obj.contractor == request.user