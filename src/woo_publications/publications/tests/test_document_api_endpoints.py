from uuid import uuid4

from django.test import override_settings
from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.api.tests.mixins import APIKeyUnAuthorizedMixin, TokenAuthMixin
from woo_publications.config.models import GlobalConfiguration
from woo_publications.contrib.documents_api.client import get_client
from woo_publications.contrib.documents_api.tests.factories import ServiceFactory
from woo_publications.metadata.tests.factories import InformationCategoryFactory
from woo_publications.utils.tests.vcr import VCRMixin

from ..models import Document
from .factories import DocumentFactory, PublicationFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class DocumentApiAuthorizationAndPermissionTests(APIKeyUnAuthorizedMixin, APITestCase):
    def test_403_when_audit_headers_are_missing(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        list_endpoint = reverse("api:document-list")
        detail_endpoint = reverse("api:document-detail", kwargs={"uuid": str(uuid4())})

        with self.subTest(action="list"):
            response = self.client.get(list_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with self.subTest(action="retrieve"):
            response = self.client.get(detail_endpoint, headers={})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_key_result_in_301_with_wrong_credentials(self):
        document = DocumentFactory.create()
        list_url = reverse("api:document-list")
        detail_url = reverse(
            "api:document-detail",
            kwargs={"uuid": str(document.uuid)},
        )

        self.assertWrongApiKeyProhibitsGetEndpointAccess(list_url)
        self.assertWrongApiKeyProhibitsGetEndpointAccess(detail_url)


class DocumentApiReadTests(TokenAuthMixin, APITestCase):
    def test_list_documents(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            document = DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            document2 = DocumentFactory.create(
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
                "uuid": str(document2.uuid),
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
                "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
                "bestandsdelen": None,
            }

            self.assertEqual(data["results"][0], expected_second_item_data)

        with self.subTest("second_item_in_response_with_expected_data"):
            expected_first_item_data = {
                "uuid": str(document.uuid),
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
                "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
                "bestandsdelen": None,
            }

            self.assertEqual(data["results"][1], expected_first_item_data)

    def test_list_documents_filter_order(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            document = DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        with freeze_time("2024-09-24T12:00:00-00:00"):
            document2 = DocumentFactory.create(
                publicatie=publication2,
                identifier="document-2",
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
                creatiedatum="2024-02-02",
            )

        expected_first_item_data = {
            "uuid": str(document.uuid),
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
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
            "bestandsdelen": None,
        }
        expected_second_item_data = {
            "uuid": str(document2.uuid),
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
            "laatstGewijzigdDatum": "2024-09-24T14:00:00+02:00",
            "bestandsdelen": None,
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
            document = DocumentFactory.create(
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
            "uuid": str(document.uuid),
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
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
            "bestandsdelen": None,
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

    def test_list_document_identifier_filter(self):
        publication, publication2 = PublicationFactory.create_batch(2)
        with freeze_time("2024-09-25T12:30:00-00:00"):
            document = DocumentFactory.create(
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
            "uuid": str(document.uuid),
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
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
            "bestandsdelen": None,
        }

        response = self.client.get(
            reverse("api:document-list"),
            {"identifier": "document-1"},
            headers=AUDIT_HEADERS,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0], expected_first_item_data)

    def test_detail_document(self):
        publication = PublicationFactory.create()
        with freeze_time("2024-09-25T12:30:00-00:00"):
            document = DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                creatiedatum="2024-01-01",
            )
        detail_url = reverse(
            "api:document-detail",
            kwargs={"uuid": str(document.uuid)},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        expected_data = {
            "uuid": str(document.uuid),
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
            "laatstGewijzigdDatum": "2024-09-25T14:30:00+02:00",
            "bestandsdelen": None,
        }

        self.assertEqual(data, expected_data)


@override_settings(ALLOWED_HOSTS=["testserver", "host.docker.internal"])
class DocumentApiCreateTests(VCRMixin, TokenAuthMixin, APITestCase):
    """
    Test the Document create (POST) endpoint.

    WOO Publications acts as a bit of a proxy - a document that gets created/registered
    with us is saved into the Documents API, primarily to handle the file uploads
    accordingly.

    The API traffic is captured and 'mocked' using VCR.py. When re-recording the cassettes
    for these tests, make sure to bring up the docker compose in the root of the repo:

    .. code-block:: bash

        docker compose up

    See ``docker/open-zaak/README.md`` for the test credentials and available data.

    Note that we make use of the information categories fixture, which gets loaded in
    the WOO Publications backend automatically. See the file
    ``/home/bbt/code/gpp-woo/woo-publications/src/woo_publications/fixtures/information_categories.json``
    for the reference.

    The flow of requests is quite complex here in this test setup - an alternative
    setup with live server test case would also work, but that's trading one flavour
    of complexity for another (and it's quite a bit slower + harder to debug issues).
    The diagram below describes which requests are handled by which part. The parts
    are:

    * TestClient: ``self.client`` in this test case
    * Woo-P: the code/api endpoints being tested, what we're used to in DRF testing
    * Docker Open Zaak: the Open Zaak instance from the root docker-compose.yml
    * Docker Woo-P: the Woo-P instance from the root docker-compose.yml. Most notably,
      this is the same component but a different instance of Woo-P.

    .. code-block:: none

        TestClient::document-create -> Woo-P:DRF endpoint  ------------+
                                                                       |
        +--- Docker Open Zaak::enkelvoudiginformatieobject-create  <---+
        |
        +--> Docker Woo-P::informatieobjecttype-read
    """

    # this UUID is in the fixture
    DOCUMENT_TYPE_UUID = "9aeb7501-3f77-4f36-8c8f-d21f47c2d6e8"
    DOCUMENT_TYPE_URL = (
        "http://host.docker.internal:8000/catalogi/api/v1/informatieobjecttypen/"
        + DOCUMENT_TYPE_UUID
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Set up global configuration
        cls.service = service = ServiceFactory.create(
            for_documents_api_docker_compose=True
        )
        config = GlobalConfiguration.get_solo()
        config.documents_api_service = service
        config.organisation_rsin = "000000000"
        config.save()

        cls.information_category = InformationCategoryFactory.create(
            uuid=cls.DOCUMENT_TYPE_UUID
        )

    def setUp(self):
        super().setUp()
        self.addCleanup(GlobalConfiguration.clear_cache)

    def test_create_document_results_in_document_in_external_api(self):
        publication = PublicationFactory.create(
            informatie_categorieen=[self.information_category]
        )
        endpoint = reverse("api:document-list")
        body = {
            "identifier": "WOO-P/0042",
            "publicatie": publication.uuid,
            "officieleTitel": "Testdocument WOO-P + Open Zaak",
            "verkorteTitel": "Testdocument",
            "omschrijving": "Testing 123",
            "creatiedatum": "2024-11-05",
            "bestandsformaat": "unknown",
            "bestandsnaam": "unknown.bin",
            "bestandsomvang": 10,
        }

        response = self.client.post(
            endpoint,
            data=body,
            headers={
                **AUDIT_HEADERS,
                "Host": "host.docker.internal:8000",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with self.subTest("expected woo-publications state"):
            document = Document.objects.get()
            self.assertNotEqual(document.lock, "")
            self.assertEqual(document.document_service, self.service)
            self.assertIsNotNone(document.document_uuid)

            # check that we have one file part in the response
            file_parts = response.json()["bestandsdelen"]
            self.assertEqual(len(file_parts), 1)

        # check that we can look up the document in the Open Zaak API:
        with (
            self.subTest("expected documents API state"),
            get_client(document.document_service) as client,
        ):
            detail = client.get(
                f"enkelvoudiginformatieobjecten/{document.document_uuid}"
            )
            self.assertEqual(detail.status_code, status.HTTP_200_OK)
            detail_data = detail.json()
            self.assertTrue(detail_data["locked"])
