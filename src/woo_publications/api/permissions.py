from rest_framework.permissions import BasePermission


class AuditHeaderPermission(BasePermission):
    AUDIT_HEADERS = [
        "HTTP_AUDIT_USER_REPRESENTATION",
        "HTTP_AUDIT_USER_ID",
        "HTTP_AUDIT_REMARKS",
    ]

    def has_permission(self, request, view):
        for header in self.AUDIT_HEADERS:
            if header not in request.META:
                return False
        return True
