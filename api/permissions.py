from rest_framework import permissions

class IsOwnerOrReadyOnly(permissions.BasePermission):
    """
    Custom permission to only allow Players who are associated with the
    `created_by` attribute of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Always allow GET, HEAD, and OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Restrict write permissions to `created_by` Player
        return obj.created_by == request.user