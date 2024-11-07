from uuid import uuid4

from django.urls import reverse
from django.utils.translation import gettext as _

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.api.tests.mixins import APIKeyUnAuthorizedMixin, TokenAuthMixin
from woo_publications.logging.logevent import audit_api_create
from woo_publications.logging.serializing import serialize_instance
from woo_publications.metadata.tests.factories import (
    InformationCategoryFactory,
    OrganisationFactory,
)

from ..models import Publication
from .factories import PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class PublicationApiAuthorizationAndPermissionTests(
    APIKeyUnAuthorizedMixin, APITestCase
):
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

    def test_api_key_result_in_401_with_wrong_credentials(self):
        publication = PublicationFactory.create()
        list_url = reverse("api:publication-list")
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )

        # create
        self.assertWrongApiKeyProhibitsPostEndpointAccess(detail_url)
        # read
        self.assertWrongApiKeyProhibitsGetEndpointAccess(list_url)
        self.assertWrongApiKeyProhibitsGetEndpointAccess(detail_url)
        # update
        self.assertWrongApiKeyProhibitsPatchEndpointAccess(detail_url)
        self.assertWrongApiKeyProhibitsPutEndpointAccess(detail_url)
        # delete
        self.assertWrongApiKeyProhibitsDeleteEndpointAccess(detail_url)


class PublicationApiTests(TokenAuthMixin, APITestCase):
    def test_list_publications(self):
        ic, ic2 = InformationCategoryFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication2 = PublicationFactory.create(
                informatie_categorieen=[ic2],
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
                "informatieCategorieen": [str(ic.uuid)],
                "publisher": str(publication.publisher.uuid),
                "verantwoordelijke": None,
                "opsteller": None,
                "officieleTitel": "title one",
                "verkorteTitel": "one",
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "eigenaar": None,
                "registratiedatum": "2024-09-25T14:30:00+02:00",
                "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
            }

            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_second_item_data = {
                "uuid": str(publication2.uuid),
                "informatieCategorieen": [str(ic2.uuid)],
                "publisher": str(publication2.publisher.uuid),
                "verantwoordelijke": None,
                "opsteller": None,
                "officieleTitel": "title two",
                "verkorteTitel": "two",
                "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                "eigenaar": None,
                "registratiedatum": "2024-09-24T14:00:00+02:00",
                "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
            }

            self.assertEqual(data["results"][1], expected_second_item_data)

    def test_list_publications_filter_order(self):
        ic, ic2 = InformationCategoryFactory.create_batch(2)
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = PublicationFactory.create(
                informatie_categorieen=[ic2],
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
        expected_first_item_data = {
            "uuid": str(publication.uuid),
            "informatieCategorieen": [str(ic.uuid)],
            "publisher": str(publication.publisher.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "eigenaar": None,
            "registratiedatum": "2024-09-24T14:00:00+02:00",
            "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
        }
        expected_second_item_data = {
            "uuid": str(publication2.uuid),
            "informatieCategorieen": [str(ic2.uuid)],
            "publisher": str(publication2.publisher.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "title two",
            "verkorteTitel": "two",
            "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            "eigenaar": None,
            "registratiedatum": "2024-09-25T14:30:00+02:00",
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
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

    def test_list_publications_filter_owner(self):
        ic, ic2 = InformationCategoryFactory.create_batch(2)
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                informatie_categorieen=[ic],
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
            # mimicking creating log though api
            audit_api_create(
                content_object=publication,
                user_id="123",
                user_display="buurman",
                object_data=serialize_instance(publication),
                remarks="test",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = PublicationFactory.create(
                informatie_categorieen=[ic2],
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
            # mimicking creating log though api
            audit_api_create(
                content_object=publication2,
                user_id="456",
                user_display="buurman",
                object_data=serialize_instance(publication2),
                remarks="test",
            )

        expected_first_item_data = {
            "uuid": str(publication.uuid),
            "informatieCategorieen": [str(ic.uuid)],
            "publisher": str(publication.publisher.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "eigenaar": {"weergaveNaam": "buurman", "identifier": "123"},
            "registratiedatum": "2024-09-24T14:00:00+02:00",
            "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
        }
        expected_second_item_data = {
            "uuid": str(publication2.uuid),
            "informatieCategorieen": [str(ic2.uuid)],
            "publisher": str(publication2.publisher.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "title two",
            "verkorteTitel": "two",
            "omschrijving": "Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            "eigenaar": {"weergaveNaam": "buurman", "identifier": "456"},
            "registratiedatum": "2024-09-25T14:30:00+02:00",
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
        }

        with (
            self.subTest("filter_with_existing_eigenaar"),
            freeze_time("2024-10-01T00:00:00-00:00"),
        ):
            response = self.client.get(
                reverse("api:publication-list"),
                {"eigenaar": "123"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["count"], 1)
            self.assertEqual(data["results"][0], expected_first_item_data)

        with self.subTest("filter_with_none_existing_eigenaar"):
            response = self.client.get(
                reverse("api:publication-list"),
                {"eigenaar": "39834594397543"},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["count"], 0)

        with (
            self.subTest("filter_with_no_input"),
            freeze_time("2024-10-01T00:00:00-00:00"),
        ):
            response = self.client.get(
                reverse("api:publication-list"),
                {"eigenaar": ""},
                headers=AUDIT_HEADERS,
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = response.json()

            self.assertEqual(data["count"], 2)

            self.assertEqual(data["results"][0], expected_second_item_data)
            self.assertEqual(data["results"][1], expected_first_item_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_detail_publication(self):
        ic = InformationCategoryFactory.create()
        publication = PublicationFactory.create(
            informatie_categorieen=[ic],
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
            "informatieCategorieen": [str(ic.uuid)],
            "publisher": str(publication.publisher.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "title one",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "eigenaar": None,
            "registratiedatum": "2024-09-24T14:00:00+02:00",
            "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
        }

        self.assertEqual(data, expected_first_item_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_create_publication(self):
        ic, ic2 = InformationCategoryFactory.create_batch(2)
        organisation, organisation2, organisation3 = OrganisationFactory.create_batch(
            3, is_actief=True
        )
        deactivated_organisation = OrganisationFactory.create(is_actief=False)
        url = reverse("api:publication-list")

        with self.subTest("no information categories results in error"):
            data = {
                "officieleTitel": "bla",
                "verkorteTitel": "bla",
                "omschrijving": "bla",
            }

            response = self.client.post(url, data, headers=AUDIT_HEADERS)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["informatieCategorieen"], [_("This field is required.")]
            )

        with self.subTest("deactivated organisation cannot be used as an organisation"):
            data = {
                "publisher": str(deactivated_organisation.uuid),
                "verantwoordelijke": str(deactivated_organisation.uuid),
                "opsteller": str(deactivated_organisation.uuid),
            }

            response = self.client.post(url, data, headers=AUDIT_HEADERS)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()

            # format the same way drf does for gettext to translate the error message properly
            self.assertEqual(
                response_data["publisher"],
                [
                    _("Object with {slug_name}={value} does not exist.").format(
                        slug_name="uuid", value=deactivated_organisation.uuid
                    )
                ],
            )
            self.assertEqual(
                response_data["verantwoordelijke"],
                [
                    _("Object with {slug_name}={value} does not exist.").format(
                        slug_name="uuid", value=deactivated_organisation.uuid
                    )
                ],
            )
            self.assertNotIn(
                "opsteller",
                response_data,
            )

        with self.subTest("no publisher results in error"):
            data = {
                "informatieCategorieen": [str(ic.uuid)],
                "officieleTitel": "bla",
                "verkorteTitel": "bla",
                "omschrijving": "bla",
            }

            response = self.client.post(url, data, headers=AUDIT_HEADERS)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(response_data["publisher"], [_("This field is required.")])

        with self.subTest("complete data"):
            data = {
                "informatieCategorieen": [str(ic.uuid), str(ic2.uuid)],
                "publisher": str(organisation.uuid),
                "verantwoordelijke": str(organisation2.uuid),
                "opsteller": str(organisation3.uuid),
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
                "informatieCategorieen": [str(ic.uuid), str(ic2.uuid)],
                "publisher": str(organisation.uuid),
                "verantwoordelijke": str(organisation2.uuid),
                "opsteller": str(organisation3.uuid),
                "officieleTitel": "title one",
                "verkorteTitel": "one",
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "eigenaar": {"weergaveNaam": "username", "identifier": "id"},
                "registratiedatum": "2024-09-24T14:00:00+02:00",
                "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
            }

            self.assertEqual(response_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_update_publication(self):
        ic, ic2 = InformationCategoryFactory.create_batch(2)
        organisation, organisation2, organisation3 = OrganisationFactory.create_batch(
            3, is_actief=True
        )
        publication = PublicationFactory.create(
            informatie_categorieen=[ic, ic2],
            publisher=organisation3,
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        detail_url = reverse(
            "api:publication-detail",
            kwargs={"uuid": str(publication.uuid)},
        )

        with self.subTest("empty information categories results in error"):
            data = {
                "officieleTitel": "changed offical title",
                "verkorteTitel": "changed short title",
                "omschrijving": "changed description",
            }

            response = self.client.put(detail_url, data, headers=AUDIT_HEADERS)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response_data = response.json()
            self.assertEqual(
                response_data["informatieCategorieen"], [_("This field is required.")]
            )

        with self.subTest("complete data"):

            data = {
                "informatieCategorieen": [str(ic2.uuid)],
                "publisher": str(organisation.uuid),
                "verantwoordelijke": str(organisation2.uuid),
                "opsteller": str(organisation3.uuid),
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
                "informatieCategorieen": [str(ic2.uuid)],
                "publisher": str(organisation.uuid),
                "verantwoordelijke": str(organisation2.uuid),
                "opsteller": str(organisation3.uuid),
                "officieleTitel": "changed offical title",
                "verkorteTitel": "changed short title",
                "omschrijving": "changed description",
                "eigenaar": None,
                "registratiedatum": "2024-09-24T14:00:00+02:00",
                "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
            }

            self.assertEqual(response_data, expected_data)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_partial_update_publication(self):
        ic = InformationCategoryFactory.create()
        organisation = OrganisationFactory.create(is_actief=True)
        publication = PublicationFactory.create(
            informatie_categorieen=[ic],
            publisher=organisation,
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

        response = self.client.patch(detail_url, data, headers=AUDIT_HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        expected_data = {
            "uuid": response_data[
                "uuid"
            ],  # uuid gets generated so we are just testing that its there
            "informatieCategorieen": [str(ic.uuid)],
            "publisher": str(organisation.uuid),
            "verantwoordelijke": None,
            "opsteller": None,
            "officieleTitel": "changed offical title",
            "verkorteTitel": "one",
            "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "eigenaar": None,
            "registratiedatum": "2024-09-24T14:00:00+02:00",
            "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
        }

        # test that only officiele_titel got changed
        self.assertEqual(response_data, expected_data)

    def test_destroy_publication(self):
        ic = InformationCategoryFactory.create()
        publication = PublicationFactory.create(
            informatie_categorieen=[ic],
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
