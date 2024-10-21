from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from woo_publications.api.drf_spectacular.headers import ALL_AUDIT_PARAMETERS

if TYPE_CHECKING:
    from rest_framework.views import APIView


class AuditHeaderPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        required_headers = [
            parameter["name"]
            for parameter in ALL_AUDIT_PARAMETERS
            if parameter["required"]
        ]
        return all(header in request.headers for header in required_headers)
