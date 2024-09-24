from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ThemeFactory


class ThemeTests(APITestCase):
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

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        expected_second_item_data = {
            "uuid": str(child_theme.uuid),
            "identifier": "https://www.example.com/thema/2",
            "naam": "second item",
            "subThemes": [],
            "depth": 2,
        }

        expected_first_item_data = {
            "uuid": str(parent_theme.uuid),
            "identifier": "https://www.example.com/thema/1",
            "naam": "first item",
            "subThemes": [
                expected_second_item_data,
            ],
            "depth": 1,
        }

        with self.subTest("first_item_in_response_with_expected_data"):
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            self.assertEqual(data["results"][1], expected_second_item_data)

    def test_detail_theme(self):
        theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="item one",
        )
        list_url = reverse(
            "api:theme-detail",
            kwargs={"uuid": str(theme.uuid)},
        )

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        expected_data = {
            "uuid": str(theme.uuid),
            "identifier": "https://www.example.com/thema/1",
            "naam": "item one",
            "subThemes": [],
            "depth": 1,
        }

        self.assertEqual(data, expected_data)
