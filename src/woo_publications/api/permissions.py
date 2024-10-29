from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from woo_publications.api.drf_spectacular.headers import ALL_AUDIT_PARAMETERS

from .constants import PermissionOptions
from .models import TokenAuth

if TYPE_CHECKING:
    from rest_framework.views import APIView


class AuditHeaderPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        required_headers = [
            parameter.name for parameter in ALL_AUDIT_PARAMETERS if parameter.required
        ]
        return all(header in request.headers for header in required_headers)


class TokenAuthPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        token = request.auth

        if not isinstance(token, TokenAuth):
            return False

        if (
            request.method in SAFE_METHODS
            and PermissionOptions.read in token.permissies
        ):
            return True

        if (
            request.method not in SAFE_METHODS
            and PermissionOptions.write in token.permissies
        ):
            return True

        return False
