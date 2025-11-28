from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDevice(BasePermission):
    """Seuls les appareils (simulator) authentifiés peuvent POST des lectures"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.method == "POST"
        )


class IsAdminOrReadOnly(BasePermission):
    """Admin peut tout faire, les autres seulement lire"""
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )