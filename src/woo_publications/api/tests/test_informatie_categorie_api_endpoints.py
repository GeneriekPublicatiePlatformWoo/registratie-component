from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.metadata.constants import InformatieCategorieOrigins
from woo_publications.metadata.tests.factories import InformatieCategorieFactory


class InformatieCategorieTests(APITestCase):
    def setUp(self):
        self.information_category_value_list = InformatieCategorieFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            naam_meervoud="first items",
            definitie="This is some information about the first item.",
            order=0,
            oorsprong=InformatieCategorieOrigins.value_list,
        )
        self.information_category_custom_entry = InformatieCategorieFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            naam_meervoud="second items",
            definitie="This is some information about the second item.",
            order=1,
            oorsprong=InformatieCategorieOrigins.custom_entry,
        )
        super().setUp()

    def test_list_informatie_categorie(self):
        list_url = reverse("api:informatiecategorie-list")
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        # First item
        self.assertEqual(
            data["results"][0]["identifier"], "https://www.example.com/waardenlijsten/1"
        )
        self.assertEqual(data["results"][0]["naam"], "first item")
        self.assertEqual(data["results"][0]["naamMeervoud"], "first items")
        self.assertEqual(
            data["results"][0]["definitie"],
            "This is some information about the first item.",
        )
        self.assertEqual(data["results"][0]["order"], 0)
        self.assertEqual(
            data["results"][0]["oorsprong"], InformatieCategorieOrigins.value_list
        )

        # Second item
        self.assertEqual(
            data["results"][1]["identifier"], "https://www.example.com/waardenlijsten/2"
        )
        self.assertEqual(data["results"][1]["naam"], "second item")
        self.assertEqual(data["results"][1]["naamMeervoud"], "second items")
        self.assertEqual(
            data["results"][1]["definitie"],
            "This is some information about the second item.",
        )
        self.assertEqual(data["results"][1]["order"], 1)
        self.assertEqual(
            data["results"][1]["oorsprong"], InformatieCategorieOrigins.custom_entry
        )

    def test_list_informatie_categorie_search_on_identifier(self):
        list_url = reverse("api:informatiecategorie-list")
        response = self.client.get(
            list_url, {"identifier": "https://www.example.com/waardenlijsten/1"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

        # First item
        self.assertEqual(
            data["results"][0]["identifier"], "https://www.example.com/waardenlijsten/1"
        )
        self.assertEqual(data["results"][0]["naam"], "first item")
        self.assertEqual(data["results"][0]["naamMeervoud"], "first items")
        self.assertEqual(
            data["results"][0]["definitie"],
            "This is some information about the first item.",
        )
        self.assertEqual(data["results"][0]["order"], 0)
        self.assertEqual(
            data["results"][0]["oorsprong"], InformatieCategorieOrigins.value_list
        )

        with self.subTest("with_none_existing_identifier"):
            response = self.client.get(
                list_url, {"identifier": "https://www.example.com/waardenlijsten/999"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_list_informatie_categorie_search_on_naam(self):
        list_url = reverse("api:informatiecategorie-list")
        response = self.client.get(list_url, {"naam": "second item"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)

        # Second item
        self.assertEqual(
            data["results"][0]["identifier"], "https://www.example.com/waardenlijsten/2"
        )
        self.assertEqual(data["results"][0]["naam"], "second item")
        self.assertEqual(data["results"][0]["naamMeervoud"], "second items")
        self.assertEqual(
            data["results"][0]["definitie"],
            "This is some information about the second item.",
        )
        self.assertEqual(data["results"][0]["order"], 1)
        self.assertEqual(
            data["results"][0]["oorsprong"], InformatieCategorieOrigins.custom_entry
        )

        with self.subTest("with_none_existing_naam"):
            response = self.client.get(list_url, {"naam": "doesn't exist"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()
            self.assertEqual(data["count"], 0)

    def test_detail_informatie_categorie(self):
        list_url = reverse(
            "api:informatiecategorie-detail",
            kwargs={"pk": self.information_category_value_list.pk},
        )
        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # First item
        self.assertEqual(data["identifier"], "https://www.example.com/waardenlijsten/1")
        self.assertEqual(data["naam"], "first item")
        self.assertEqual(data["naamMeervoud"], "first items")
        self.assertEqual(
            data["definitie"], "This is some information about the first item."
        )
        self.assertEqual(data["order"], 0)
        self.assertEqual(data["oorsprong"], InformatieCategorieOrigins.value_list)
