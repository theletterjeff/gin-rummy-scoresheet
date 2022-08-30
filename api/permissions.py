from rest_framework import permissions

class IsRequestUser(permissions.BasePermission):
    """Custom permission for editing Player instances; you have to be the
    Player to edit.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user