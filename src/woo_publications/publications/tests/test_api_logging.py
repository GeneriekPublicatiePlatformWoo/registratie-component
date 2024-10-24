from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.logging.models import TimelineLogProxy

from ..models import Publication
from .factories import PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class PublicationLoggingTests(APITestCase):

    def test_detail_logging(self):
        assert not TimelineLogProxy.objects.exists()
        with freeze_time("2024-09-24T12:00:00-00:00"):
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
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": "read",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "_cached_object_repr": "title one",
        }
        self.assertEqual(log.extra_data, expected_data)

    def test_create_logging(self):
        assert not TimelineLogProxy.objects.exists()
        url = reverse("api:publication-list")
        data = {
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }

        with freeze_time("2024-09-24T12:00:00-00:00"):
            response = self.client.post(url, data, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        log = TimelineLogProxy.objects.get()
        publication = Publication.objects.get()
        expected_data = {
            "event": "create",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.pk,
                "uuid": response.json()["uuid"],
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "verkorte_titel": "one",
                "officiele_titel": "title one",
                "registratiedatum": "2024-09-24T12:00:00Z",
            },
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_update_publication(self):
        assert not TimelineLogProxy.objects.exists()
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
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": "update",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.pk,
                "uuid": response.json()["uuid"],
                "omschrijving": "changed description",
                "verkorte_titel": "changed short title",
                "officiele_titel": "changed offical title",
                "registratiedatum": "2024-09-24T12:00:00Z",
            },
            "_cached_object_repr": "changed offical title",
        }
        self.assertEqual(log.extra_data, expected_data)

    def test_destroy_publication(self):
        assert not TimelineLogProxy.objects.exists()
        with freeze_time("2024-09-24T12:00:00-00:00"):
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
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": "delete",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.id,
                "uuid": str(publication.uuid),
                "omschrijving": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                ),
                "verkorte_titel": "one",
                "officiele_titel": "title one",
                "registratiedatum": "2024-09-24T12:00:00Z",
            },
            "_cached_object_repr": "title one",
        }
        self.assertEqual(log.extra_data, expected_data)
