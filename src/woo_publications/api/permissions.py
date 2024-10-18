from rest_framework.permissions import BasePermission


class AuditHeaderPermission(BasePermission):
    AUDIT_HEADERS = [
        "AUDIT_USER_REPRESENTATION",
        "AUDIT_USER_ID",
        "AUDIT_REMARKS",
    ]

    def has_permission(self, request, view):
        for header in self.AUDIT_HEADERS:
            if header not in request.headers:
                return False
        return True
