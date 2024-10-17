import uuid

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ThemeFactory


class ThemeTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.headers = {
            "AUDIT_USER_REPRESENTATION": "username",
            "AUDIT_USER_ID": "id",
            "AUDIT_REMARKS": "remark",
        }

    def test_list_theme(self):
        parent_theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="first item",
        )
        child_theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/2",
            naam="second item",
            parent=parent_theme,
        )
        list_url = reverse("api:theme-list")

        response = self.client.get(list_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

        expected_second_item_data = {
            "uuid": str(child_theme.uuid),
            "identifier": "https://www.example.com/thema/2",
            "naam": "second item",
            "subThemes": [],
        }

        expected_first_item_data = {
            "uuid": str(parent_theme.uuid),
            "identifier": "https://www.example.com/thema/1",
            "naam": "first item",
            "subThemes": [
                expected_second_item_data,
            ],
        }

        with self.subTest("first_item_in_response_with_expected_data"):
            self.assertEqual(data["results"][0], expected_first_item_data)

    def test_detail_theme(self):
        theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="item one",
        )
        list_url = reverse(
            "api:theme-detail",
            kwargs={"uuid": str(theme.uuid)},
        )

        response = self.client.get(list_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        expected_data = {
            "uuid": str(theme.uuid),
            "identifier": "https://www.example.com/thema/1",
            "naam": "item one",
            "subThemes": [],
        }

        self.assertEqual(data, expected_data)

    def test_detail_theme_wrong_uuid(self):
        list_url = reverse(
            "api:theme-detail",
            kwargs={"uuid": str(uuid.uuid4)},
        )

        response = self.client.get(list_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_broken_uuid(self):
        # UUID misses 3 characters
        list_url = reverse(
            "api:theme-detail",
            kwargs={"uuid": "d6323f56-5331-4b43-8e8c-63509be1e"},
        )

        response = self.client.get(list_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
