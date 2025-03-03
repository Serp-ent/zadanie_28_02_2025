from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """Permission to allow only unauthenticated users."""

    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.user == obj:
            return True