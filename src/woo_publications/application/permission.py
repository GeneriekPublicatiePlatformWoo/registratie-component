from rest_framework.permissions import SAFE_METHODS, BasePermission

from .constants import PermissionOptions
from .models import TokenAuth

UNSAFE_METHODS = (
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
)


class TokenAuthPermission(BasePermission):
    def _check_permission(self, request) -> bool:
        token: TokenAuth = request.auth

        if not token:
            return False

        if (
            request.method in SAFE_METHODS
            and PermissionOptions.read in token.permissies
        ):
            return True

        if (
            request.method in UNSAFE_METHODS
            and PermissionOptions.write in token.permissies
        ):
            return True

        return False

    def has_permission(self, request, view) -> bool:
        return self._check_permission(request)

    def has_object_permission(self, request, view, obj) -> bool:
        return self._check_permission(request)
