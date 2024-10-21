from rest_framework import views
from rest_framework.test import APIRequestFactory, APISimpleTestCase

from ..drf_spectacular.headers import ALL_AUDIT_PARAMETERS
from ..permissions import AuditHeaderPermission

request_factory = APIRequestFactory()


class AuditHeadersPermissionTests(APISimpleTestCase):
    def test_api_call_with_all_audit_headers_passes(self):
        request = request_factory.get(
            "/irrelevant",
            headers={
                "Audit-User-Representation": "test",
                "Audit-User-ID": "test",
                "Audit-Remarks": "test",
            },
        )
        view = views.APIView()
        permission = AuditHeaderPermission()

        result = permission.has_permission(request, view)

        self.assertTrue(result)

    def test_api_call_with_one_audit_header_results_in_403(self):
        for single_header in [
            header.name for header in ALL_AUDIT_PARAMETERS if header.required
        ]:
            with self.subTest(header=single_header):
                request = request_factory.get(
                    "/irrelevant", headers={single_header: "test"}
                )
                view = views.APIView()
                permission = AuditHeaderPermission()

                result = permission.has_permission(request, view)

                self.assertFalse(result)

    def test_api_call_with_no_audit_header_results_in_403(self):
        request = request_factory.get("/irrelevant")
        view = views.APIView()
        permission = AuditHeaderPermission()

        result = permission.has_permission(request, view)

        self.assertFalse(result)
