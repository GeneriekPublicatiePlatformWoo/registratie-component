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
        ThemeFactory.create(
            identifier="https://www.example.com/thema/2",
            naam="second item",
            parent=parent_theme,
        )
        list_url = reverse("api:theme-list")

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        with self.subTest("first_item_in_response_with_expected_data"):
            expected_first_item_data = {
                "identifier": "https://www.example.com/thema/1",
                "naam": "first item",
                "depth": 1,
            }
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_second_item_data = {
                "identifier": "https://www.example.com/thema/2",
                "naam": "second item",
                "depth": 2,
            }
            self.assertEqual(data["results"][1], expected_second_item_data)

    def test_list_theme_search_on_identifier(self):
        parent_theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="first item",
        )
        ThemeFactory.create(
            identifier="https://www.example.com/thema/2",
            naam="second item",
            parent=parent_theme,
        )
        list_url = reverse("api:theme-list")

        with self.subTest("test_with_exact_match"):
            expected_first_item_data = {
                "identifier": "https://www.example.com/thema/1",
                "naam": "first item",
                "depth": 1,
            }

            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/thema/1"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("with_none_existing_identifier"):
            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/thema/999"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_list_theme_search_on_naam(self):
        parent_theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="item one",
        )
        ThemeFactory.create(
            identifier="https://www.example.com/thema/2",
            naam="item two",
            parent=parent_theme,
        )
        list_url = reverse("api:theme-list")

        expected_first_item_data = {
            "identifier": "https://www.example.com/thema/1",
            "naam": "item one",
            "depth": 1,
        }

        expected_second_item_data = {
            "identifier": "https://www.example.com/thema/2",
            "naam": "item two",
            "depth": 2,
        }

        with self.subTest("test_with_exact_match"):
            response = self.client.get(list_url, {"naam": "item two"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_second_item_data)

        with self.subTest("test_incomplete_match"):
            response = self.client.get(list_url, {"naam": "item"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("with_none_existing_naam"):
            response = self.client.get(list_url, {"naam": "item three"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_list_theme_search_on_super_theme(self):
        parent_theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="first item",
        )
        ThemeFactory.create(
            identifier="https://www.example.com/thema/2",
            naam="second item",
            parent=parent_theme,
        )
        list_url = reverse("api:theme-list")

        with self.subTest("test_on_super_theme_true"):
            expected_data = {
                "identifier": "https://www.example.com/thema/1",
                "naam": "first item",
                "depth": 1,
            }

            response = self.client.get(list_url, {"super": True})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_data)

        with self.subTest("test_on_super_theme_false"):
            expected_data = {
                "identifier": "https://www.example.com/thema/2",
                "naam": "second item",
                "depth": 2,
            }

            response = self.client.get(list_url, {"super": False})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_data)

    def test_detail_theme(self):
        theme = ThemeFactory.create(
            identifier="https://www.example.com/thema/1",
            naam="item one",
        )
        list_url = reverse(
            "api:theme-detail",
            kwargs={"pk": theme.pk},
        )

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        expected_data = {
            "identifier": "https://www.example.com/thema/1",
            "naam": "item one",
            "depth": 1,
        }

        self.assertEqual(data, expected_data)
