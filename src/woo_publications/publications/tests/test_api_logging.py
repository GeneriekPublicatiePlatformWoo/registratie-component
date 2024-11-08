from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.api.tests.mixins import TokenAuthMixin
from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy
from woo_publications.metadata.tests.factories import (
    InformationCategoryFactory,
    OrganisationFactory,
)

from ..constants import PublicationStatusOptions
from ..models import Publication
from .factories import DocumentFactory, PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class PublicationLoggingTests(TokenAuthMixin, APITestCase):

    def test_detail_logging(self):
        assert not TimelineLogProxy.objects.exists()
        ic = InformationCategoryFactory.create()
        organisation = OrganisationFactory.create(is_actief=True)
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                publisher=organisation,
                verantwoordelijke=organisation,
                opsteller=organisation,
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
            "event": Events.read,
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "_cached_object_repr": "title one",
        }
        self.assertEqual(log.extra_data, expected_data)

    def test_create_logging(self):
        assert not TimelineLogProxy.objects.exists()
        ic = InformationCategoryFactory.create()
        organisation = OrganisationFactory.create(is_actief=True)
        url = reverse("api:publication-list")
        data = {
            "informatieCategorieen": [str(ic.uuid)],
            "publicatiestatus": PublicationStatusOptions.concept,
            "publisher": str(organisation.uuid),
            "verantwoordelijke": str(organisation.uuid),
            "opsteller": str(organisation.uuid),
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
            "event": Events.create,
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.pk,
                "informatie_categorieen": [ic.id],
                "laatst_gewijzigd_datum": "2024-09-24T12:00:00Z",
                "officiele_titel": "title one",
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "opsteller": organisation.pk,
                "publicatiestatus": PublicationStatusOptions.concept,
                "publisher": organisation.pk,
                "registratiedatum": "2024-09-24T12:00:00Z",
                "uuid": response.json()["uuid"],
                "verantwoordelijke": organisation.pk,
                "verkorte_titel": "one",
            },
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_update_publication(self):
        assert not TimelineLogProxy.objects.exists()
        organisation = OrganisationFactory.create(is_actief=True)
        ic = InformationCategoryFactory.create()
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                publicatiestatus=PublicationStatusOptions.concept,
                publisher=organisation,
                verantwoordelijke=organisation,
                opsteller=organisation,
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )
        data = {
            "informatieCategorieen": [str(ic.uuid)],
            "publicatiestatus": PublicationStatusOptions.published,
            "publisher": str(organisation.uuid),
            "verantwoordelijke": str(organisation.uuid),
            "opsteller": str(organisation.uuid),
            "officieleTitel": "changed offical title",
            "verkorteTitel": "changed short title",
            "omschrijving": "changed description",
        }

        with freeze_time("2024-09-27T12:00:00-00:00"):
            response = self.client.put(detail_url, data, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": Events.update,
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.pk,
                "informatie_categorieen": [ic.id],
                "laatst_gewijzigd_datum": "2024-09-27T12:00:00Z",
                "officiele_titel": "changed offical title",
                "omschrijving": "changed description",
                "opsteller": organisation.pk,
                "publicatiestatus": PublicationStatusOptions.published,
                "publisher": organisation.pk,
                "registratiedatum": "2024-09-24T12:00:00Z",
                "uuid": response.json()["uuid"],
                "verantwoordelijke": organisation.pk,
                "verkorte_titel": "changed short title",
            },
            "_cached_object_repr": "changed offical title",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_destroy_publication(self):
        assert not TimelineLogProxy.objects.exists()
        ic = InformationCategoryFactory.create()
        organisation = OrganisationFactory.create(is_actief=True)
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                publicatiestatus=PublicationStatusOptions.concept,
                publisher=organisation,
                verantwoordelijke=organisation,
                opsteller=organisation,
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )

        with freeze_time("2024-09-27T12:00:00-00:00"):
            response = self.client.delete(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": Events.delete,
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "object_data": {
                "id": publication.id,
                "informatie_categorieen": [ic.id],
                "laatst_gewijzigd_datum": "2024-09-24T12:00:00Z",
                "officiele_titel": "title one",
                "omschrijving": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                ),
                "opsteller": organisation.pk,
                "publicatiestatus": PublicationStatusOptions.concept,
                "publisher": organisation.pk,
                "registratiedatum": "2024-09-24T12:00:00Z",
                "uuid": str(publication.uuid),
                "verantwoordelijke": organisation.pk,
                "verkorte_titel": "one",
            },
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)


class DocumentLoggingTests(TokenAuthMixin, APITestCase):

    def test_detail_logging(self):
        assert not TimelineLogProxy.objects.exists()
        document = DocumentFactory.create(
            officiele_titel="title one",
        )
        detail_url = reverse(
            "api:document-detail",
            kwargs={"uuid": str(document.uuid)},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log = TimelineLogProxy.objects.get()
        expected_data = {
            "event": Events.read,
            "remarks": "remark",
            "acting_user": {"identifier": "id", "display_name": "username"},
            "_cached_object_repr": "title one",
        }
        self.assertEqual(log.extra_data, expected_data)
