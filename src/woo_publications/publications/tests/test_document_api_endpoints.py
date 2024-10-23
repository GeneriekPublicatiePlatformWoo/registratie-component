from uuid import uuid4

from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.accounts.tests.factories import UserFactory

from .factories import DocumentFactory, PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class DocumentApiTests(APITestCase):
    def test_403_when_audit_headers_are_missing(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        list_endpoint = reverse("api:document-list")
        detail_endpoint = reverse(
            "api:document-detail", kwargs={"identifier": str(uuid4())}
        )

        with self.subTest(action="list"):
            response = self.client.get(list_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="retrieve"):
            response = self.client.get(detail_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_documents(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            DocumentFactory.create(
                publicatie=publication2,
                identifier="document-2",
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                creatiedatum="2024-02-02",
            )

        response = self.client.get(reverse("api:document-list"), headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        with self.subTest("first_item_in_response_with_expected_data"):
            expected_second_item_data = {
                "identifier": "document-2",
                "publicatie": str(publication2.uuid),
                "officieleTitel": "title two",
                "verkorteTitel": "two",
                "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                "creatiedatum": "2024-02-02",
                "bestandsformaat": "unknown",
                "bestandsnaam": "unknown.bin",
                "bestandsomvang": 0,
                "registratiedatum": "2024-09-24T14:00:00+02:00",
            }

            self.assertEqual(data["results"][0], expected_second_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_first_item_data = {
                "identifier": "document-1",
                "publicatie": str(publication.uuid),
                "officieleTitel": "title one",
                "verkorteTitel": "one",
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "creatiedatum": "2024-01-01",
                "bestandsformaat": "unknown",
                "bestandsnaam": "unknown.bin",
                "bestandsomvang": 0,
                "registratiedatum": "2024-09-25T14:30:00+02:00",
            }

            self.assertEqual(data["results"][1], expected_first_item_data)

    def test_list_documents_filter_order(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            DocumentFactory.create(
                publicatie=publication2,
                identifier="document-2",
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                creatiedatum="2024-02-02",
            )

        expected_first_item_data = {
            "identifier": "document-1",
            "publicatie": str(publication.uuid),
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "creatiedatum": "2024-01-01",
            "bestandsformaat": "unknown",
            "bestandsnaam": "unknown.bin",
            "bestandsomvang": 0,
            "registratiedatum": "2024-09-25T14:30:00+02:00",
        }
        expected_second_item_data = {
            "identifier": "document-2",
            "publicatie": str(publication2.uuid),
            "officieleTitel": "title two",
            "verkorteTitel": "two",
            "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            "creatiedatum": "2024-02-02",
            "bestandsformaat": "unknown",
            "bestandsnaam": "unknown.bin",
            "bestandsomvang": 0,
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }

        # registratiedatum
        with self.subTest("creatiedatum_ascending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "creatiedatum"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("creatiedatum_descending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "-creatiedatum"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

        # Officiele titel
        with self.subTest("officiele_title_ascending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "officiele_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("officiele_title_descending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "-officiele_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

        # short titel
        with self.subTest("verkorte_titel_ascending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "verkorte_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("verkorte_titel_descending"):
            response = self.client.get(
                reverse("api:document-list"),
                {"sorteer": "-verkorte_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

    def test_list_document_publication_filter(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            DocumentFactory.create(
                publicatie=publication2,
                identifier="document-2",
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                creatiedatum="2024-02-02",
            )

        expected_first_item_data = {
            "identifier": "document-1",
            "publicatie": str(publication.uuid),
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "creatiedatum": "2024-01-01",
            "bestandsformaat": "unknown",
            "bestandsnaam": "unknown.bin",
            "bestandsomvang": 0,
            "registratiedatum": "2024-09-25T14:30:00+02:00",
        }

        response = self.client.get(
            reverse("api:document-list"),
            {"publicatie": str(publication.uuid)},
            headers=AUDIT_HEADERS,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0], expected_first_item_data)

    def test_detail_document(self):
        publication = PublicationFactory.create()
        with freeze_time("2024-09-25T12:30:00-00:00"):
            DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        detail_url = reverse(
            "api:document-detail",
            kwargs={"identifier": "document-1"},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        expected_data = {
            "identifier": "document-1",
            "publicatie": str(publication.uuid),
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "creatiedatum": "2024-01-01",
            "bestandsformaat": "unknown",
            "bestandsnaam": "unknown.bin",
            "bestandsomvang": 0,
            "registratiedatum": "2024-09-25T14:30:00+02:00",
        }

        self.assertEqual(data, expected_data)
