from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..constants import InformationCategoryOrigins
from .factories import InformationCategoryFactory


class InformationCategoryTests(APITestCase):
    def test_list_informatie_categorie(self):
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            naam_meervoud="first items",
            definitie="This is some information about the first item.",
            order=0,
            oorsprong=InformationCategoryOrigins.value_list,
        )
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            naam_meervoud="second items",
            definitie="This is some information about the second item.",
            order=1,
            oorsprong=InformationCategoryOrigins.custom_entry,
        )

        list_url = reverse("api:informationcategory-list")

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        with self.subTest("first_item_in_response_with_expected_data"):
            expected_first_item_data = {
                "identifier": "https://www.example.com/waardenlijsten/1",
                "naam": "first item",
                "naamMeervoud": "first items",
                "definitie": "This is some information about the first item.",
                "order": 0,
                "oorsprong": InformationCategoryOrigins.value_list,
            }
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_second_item_data = {
                "identifier": "https://www.example.com/waardenlijsten/2",
                "naam": "second item",
                "naamMeervoud": "second items",
                "definitie": "This is some information about the second item.",
                "order": 1,
                "oorsprong": InformationCategoryOrigins.custom_entry,
            }
            self.assertEqual(data["results"][1], expected_second_item_data)

    def test_list_informatie_categorie_search_on_identifier(self):
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            naam_meervoud="first items",
            definitie="This is some information about the first item.",
            order=0,
            oorsprong=InformationCategoryOrigins.value_list,
        )
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            naam_meervoud="second items",
            definitie="This is some information about the second item.",
            order=1,
            oorsprong=InformationCategoryOrigins.custom_entry,
        )

        list_url = reverse("api:informationcategory-list")

        expected_first_item_data = {
            "identifier": "https://www.example.com/waardenlijsten/1",
            "naam": "first item",
            "naamMeervoud": "first items",
            "definitie": "This is some information about the first item.",
            "order": 0,
            "oorsprong": InformationCategoryOrigins.value_list,
        }
        expected_second_item_data = {
            "identifier": "https://www.example.com/waardenlijsten/2",
            "naam": "second item",
            "naamMeervoud": "second items",
            "definitie": "This is some information about the second item.",
            "order": 1,
            "oorsprong": InformationCategoryOrigins.custom_entry,
        }

        with self.subTest("test_with_exact_match"):
            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/waardenlijsten/1"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("test_with_incomplete_match"):
            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/waardenlij"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("with_none_existing_identifier"):
            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/waardenlijsten/999"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_list_informatie_categorie_search_on_naam(self):
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="item one",
            naam_meervoud="item one (but plural?)",
            definitie="This is some information about the item one.",
            order=0,
            oorsprong=InformationCategoryOrigins.value_list,
        )
        InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="item two",
            naam_meervoud="item two (but plural?)",
            definitie="This is some information about the item two.",
            order=1,
            oorsprong=InformationCategoryOrigins.custom_entry,
        )

        list_url = reverse("api:informationcategory-list")

        expected_item_one_data = {
            "identifier": "https://www.example.com/waardenlijsten/1",
            "naam": "item one",
            "naamMeervoud": "item one (but plural?)",
            "definitie": "This is some information about the item one.",
            "order": 0,
            "oorsprong": InformationCategoryOrigins.value_list,
        }
        expected_item_two_data = {
            "identifier": "https://www.example.com/waardenlijsten/2",
            "naam": "item two",
            "naamMeervoud": "item two (but plural?)",
            "definitie": "This is some information about the item two.",
            "order": 1,
            "oorsprong": InformationCategoryOrigins.custom_entry,
        }

        with self.subTest("test_with_exact_match"):
            response = self.client.get(list_url, {"naam": "item two"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_item_two_data)

        with self.subTest("test_with_incomplete_match"):
            response = self.client.get(list_url, {"naam": "item"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 2)
            self.assertEqual(data["results"][0], expected_item_one_data)
            self.assertEqual(data["results"][1], expected_item_two_data)

        with self.subTest("with_none_existing_identifier"):
            response = self.client.get(list_url, {"naam": "item three"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_detail_informatie_categorie(self):
        information_category = InformationCategoryFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            naam_meervoud="first items",
            definitie="This is some information about the first item.",
            order=0,
            oorsprong=InformationCategoryOrigins.value_list,
        )

        list_url = reverse(
            "api:informationcategory-detail",
            kwargs={"pk": information_category.pk},
        )
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        expected_data = {
            "identifier": "https://www.example.com/waardenlijsten/1",
            "naam": "first item",
            "naamMeervoud": "first items",
            "definitie": "This is some information about the first item.",
            "order": 0,
            "oorsprong": InformationCategoryOrigins.value_list,
        }
        self.assertEqual(data, expected_data)
