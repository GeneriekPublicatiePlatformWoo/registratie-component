from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class AuditHeadersTests(APITestCase):
    def test_api_call_with_all_audit_headers_results_in_200(self):
        list_url = reverse("api:theme-list")

        audit_headers = {
            "AUDIT_USER_REPRESENTATION": "test",
            "AUDIT_USER_ID": "test",
            "AUDIT_REMARKS": "test",
        }

        response = self.client.get(list_url, headers=audit_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_call_with_one_audit_header_results_in_403(self):
        list_url = reverse("api:theme-list")

        audit_headers = {
            "AUDIT_USER_REPRESENTATION": "test",
        }

        response = self.client.get(list_url, headers=audit_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_call_with_no_audit_header_results_in_403(self):
        list_url = reverse("api:theme-list")

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
