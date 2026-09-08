from rest_framework import permissions


class IsListingAgentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and hasattr(request.user, 'agent_profile')
        )

    def has_object_permission(self, request, view, obj):
        
        # Safe methods (GET, HEAD, OPTIONS) are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the logged-in user even has an agent profile attached
        if not request.user.is_authenticated or not hasattr(request.user, 'agent_profile'):
            return False
        
        # Check if the listing's agent matches the logged-in user's agent profile
        return obj.agent == request.user.agent_profile        
