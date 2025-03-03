from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """Permission to allow only unauthenticated users."""

    def has_permission(self, request, view):
        return not request.user.is_authenticated
