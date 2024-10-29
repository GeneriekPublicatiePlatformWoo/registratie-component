from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .factories import TokenAuthFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class APIKeyUnAuthorizedMixin:

    self: APITestCase
    client: APIClient

    def assertWrongApiKeyProhibitsGetEndpointAccess(self, url):
        no_permission_token = TokenAuthFactory.create().token
        write_token = TokenAuthFactory.create(write_permission=True).token

        with self.subTest("no token given"):  # type: ignore reportAttributeAccessIssue
            response = self.client.get(url, headers=AUDIT_HEADERS)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("none existing token"):  # type: ignore reportAttributeAccessIssue
            response = self.client.get(
                url, headers={"Authorization": "Token broken", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("token with no permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.get(
                url,
                headers={
                    "Authorization": f"Token {no_permission_token}",
                    **AUDIT_HEADERS,
                },
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        with self.subTest("token with wrong permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.get(
                url, headers={"Authorization": f"Token {write_token}", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def assertWrongApiKeyProhibitsPostEndpointAccess(self, url):
        no_permission_token = TokenAuthFactory.create().token
        read_token = TokenAuthFactory.create(read_permission=True).token

        with self.subTest("no token given"):  # type: ignore reportAttributeAccessIssue
            response = self.client.post(url, headers=AUDIT_HEADERS)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("none existing token"):  # type: ignore reportAttributeAccessIssue
            response = self.client.post(
                url, headers={"Authorization": "Token broken", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("token with no permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.post(
                url,
                headers={
                    "Authorization": f"Token {no_permission_token}",
                    **AUDIT_HEADERS,
                },
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        with self.subTest("token with wrong permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.post(
                url, headers={"Authorization": f"Token {read_token}", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def assertWrongApiKeyProhibitsPatchEndpointAccess(self, url):
        no_permission_token = TokenAuthFactory.create().token
        read_token = TokenAuthFactory.create(read_permission=True).token

        with self.subTest("no token given"):  # type: ignore reportAttributeAccessIssue
            response = self.client.patch(url, headers=AUDIT_HEADERS)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("none existing token"):  # type: ignore reportAttributeAccessIssue
            response = self.client.patch(
                url, headers={"Authorization": "Token broken", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("token with no permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.patch(
                url,
                headers={
                    "Authorization": f"Token {no_permission_token}",
                    **AUDIT_HEADERS,
                },
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        with self.subTest("token with wrong permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.patch(
                url, headers={"Authorization": f"Token {read_token}", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def assertWrongApiKeyProhibitsPutEndpointAccess(self, url):
        no_permission_token = TokenAuthFactory.create().token
        read_token = TokenAuthFactory.create(read_permission=True).token

        with self.subTest("no token given"):  # type: ignore reportAttributeAccessIssue
            response = self.client.put(url, headers=AUDIT_HEADERS)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("none existing token"):  # type: ignore reportAttributeAccessIssue
            response = self.client.put(
                url, headers={"Authorization": "Token broken", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("token with no permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.put(
                url,
                headers={
                    "Authorization": f"Token {no_permission_token}",
                    **AUDIT_HEADERS,
                },
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        with self.subTest("token with wrong permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.put(
                url, headers={"Authorization": f"Token {read_token}", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def assertWrongApiKeyProhibitsDeleteEndpointAccess(self, url):
        no_permission_token = TokenAuthFactory.create().token
        read_token = TokenAuthFactory.create(read_permission=True).token

        with self.subTest("no token given"):  # type: ignore reportAttributeAccessIssue
            response = self.client.delete(url, headers=AUDIT_HEADERS)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("none existing token"):  # type: ignore reportAttributeAccessIssue
            response = self.client.delete(
                url, headers={"Authorization": "Token broken", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        with self.subTest("token with no permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.delete(
                url,
                headers={
                    "Authorization": f"Token {no_permission_token}",
                    **AUDIT_HEADERS,
                },
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN

        with self.subTest("token with wrong permission"):  # type: ignore reportAttributeAccessIssue
            response = self.client.delete(
                url, headers={"Authorization": f"Token {read_token}", **AUDIT_HEADERS}
            )
            assert response.status_code == status.HTTP_403_FORBIDDEN


class TokenAuthMixin:
    client: APIClient

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()  # type: ignore reportAttributeAccessIssue

        cls.token_auth = TokenAuthFactory.create(read_write_permission=True)

    def setUp(self):
        super().setUp()  # type: ignore reportAttributeAccessIssue

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_auth.token}")
