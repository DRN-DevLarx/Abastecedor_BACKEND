from rest_framework.permissions import BasePermission

class IsAuthenticatedAllowInactive(BasePermission):
    """
    Permite el acceso a cualquier usuario autenticado, incluso si is_active=False
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
