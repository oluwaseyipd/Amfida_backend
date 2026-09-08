from rest_framework import permissions


class IsHostelOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and hasattr(request.user, "landlord_profile")
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated or not hasattr(request.user, 'landlord_profile'):
            return False
        
        return obj.landlord == request.user.landlord_profile