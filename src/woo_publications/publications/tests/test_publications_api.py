from uuid import uuid4

from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.accounts.tests.factories import UserFactory

from ..models import Publication
from .factories import PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class PublicationApiTests(APITestCase):
    def test_403_when_audit_headers_are_missing(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        list_endpoint = reverse("api:publication-list")
        detail_endpoint = reverse(
            "api:publication-detail", kwargs={"uuid": str(uuid4())}
        )

        with self.subTest(action="list"):
            response = self.client.get(list_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="retrieve"):
            response = self.client.get(detail_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="create"):
            response = self.client.post(list_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="update"):
            response = self.client.put(detail_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="destroy"):
            response = self.client.delete(detail_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_publications(self):
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication2 = PublicationFactory.create(
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )

        response = self.client.get(
            reverse("api:publication-list"), headers=AUDIT_HEADERS
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 2)

        with self.subTest("first_item_in_response_with_expected_data"):
            expected_first_item_data = {
                "uuid": str(publication.uuid),
                "officieleTitel": "title one",
                "verkorteTitel": "one",
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "registratiedatum": "2024-09-25T14:30:00+02:00",
            }

            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_second_item_data = {
                "uuid": str(publication2.uuid),
                "officieleTitel": "title two",
                "verkorteTitel": "two",
                "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                "registratiedatum": "2024-09-24T14:00:00+02:00",
            }

            self.assertEqual(data["results"][1], expected_second_item_data)

    def test_list_publications_filter_order(self):
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = PublicationFactory.create(
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
        expected_first_item_data = {
            "uuid": str(publication.uuid),
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }
        expected_second_item_data = {
            "uuid": str(publication2.uuid),
            "officieleTitel": "title two",
            "verkorteTitel": "two",
            "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            "registratiedatum": "2024-09-25T14:30:00+02:00",
        }

        # registratiedatum
        with self.subTest("registratiedatum_ascending"):
            response = self.client.get(
                reverse("api:publication-list"),
                {"sorteer": "registratiedatum"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("registratiedatum_descending"):
            response = self.client.get(
                reverse("api:publication-list"),
                {"sorteer": "-registratiedatum"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

        # Officiele titel
        with self.subTest("officiele_title_ascending"):
            response = self.client.get(
                reverse("api:publication-list"),
                {"sorteer": "officiele_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("officiele_title_descending"):
            response = self.client.get(
                reverse("api:publication-list"),
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
                reverse("api:publication-list"),
                {"sorteer": "verkorte_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_first_item_data)
            self.assertEqual(data["results"][1], expected_second_item_data)

        with self.subTest("verkorte_titel_descending"):
            response = self.client.get(
                reverse("api:publication-list"),
                {"sorteer": "-verkorte_titel"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_detail_publication(self):
        publication = PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        expected_first_item_data = {
            "uuid": str(publication.uuid),
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }

        self.assertEqual(data, expected_first_item_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_create_publication(self):
        url = reverse("api:publication-list")
        data = {
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }

        response = self.client.post(url, data, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        expected_data = {
            "uuid": response_data[
                "uuid"
            ],  # uuid gets generated so we are just testing that its there
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }

        self.assertEqual(response_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_update_publication(self):
        publication = PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )
        data = {
            "officieleTitel": "changed offical title",
            "verkorteTitel": "changed short title",
            "omschrijving": "changed description",
        }

        response = self.client.put(detail_url, data, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        expected_data = {
            "uuid": response_data[
                "uuid"
            ],  # uuid gets generated so we are just testing that its there
            "officieleTitel": "changed offical title",
            "verkorteTitel": "changed short title",
            "omschrijving": "changed description",
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }

        self.assertEqual(response_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_partial_update_publication(self):
        publication = PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )
        data = {
            "officieleTitel": "changed offical title",
        }

        response = self.client.put(detail_url, data, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        expected_data = {
            "uuid": response_data[
                "uuid"
            ],  # uuid gets generated so we are just testing that its there
            "officieleTitel": "changed offical title",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "registratiedatum": "2024-09-24T14:00:00+02:00",
        }

        # test that only officiele_titel got changed
        self.assertEqual(response_data, expected_data)

    def test_destroy_publication(self):
        publication = PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )

        response = self.client.delete(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Publication.objects.filter(uuid=publication.uuid).exists())
