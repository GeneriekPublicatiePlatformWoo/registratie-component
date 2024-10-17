from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.publications.tests.factories import PublicationFactory

from ..models import TimelineLogProxy


class PublicationApiTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.headers = {
            "AUDIT_USER_REPRESENTATION": "username",
            "AUDIT_USER_ID": "id",
            "AUDIT_REMARKS": "remark",
        }

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_detail_logging(self):
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

        response = self.client.get(detail_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "read",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "status_code": 200,
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_create_logging(self):
        assert not TimelineLogProxy.objects.exists()

        url = reverse("api:publication-list")
        data = {
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }

        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "create",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "uuid": response.json()["uuid"],
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "verkorte_titel": "one",
                "officiele_titel": "title one",
                "registratiedatum": "2024-09-24T14:00:00+02:00",
            },
            "status_code": 201,
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

        response = self.client.put(detail_url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "update",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "uuid": response.json()["uuid"],
                "omschrijving": "changed description",
                "verkorte_titel": "changed short title",
                "officiele_titel": "changed offical title",
                "registratiedatum": "2024-09-24T14:00:00+02:00",
            },
            "status_code": 200,
            "_cached_object_repr": "changed offical title",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_destroy_publication(self):
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

        response = self.client.delete(detail_url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "delete",
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "status_code": 204,
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)
