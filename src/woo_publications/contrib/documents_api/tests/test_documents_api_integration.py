"""
Test the high level integration with the Documents API.

These tests validate that:

* the docker-compose configuration is functional to develop against
* it's possible to register a document in the Documents API with a document type
  ('informatieobjecttype') pointing back to woo-publications

The API traffic is captured and 'mocked' using VCR.py. When re-recording the cassettes
for these tests, make sure to bring up the docker compose in the root of the repo:

.. code-block:: bash

    docker compose up

See ``docker/open-zaak/README.md`` for the test credentials and available data.
"""

from django.test import TestCase

from zgw_consumers.client import build_client
from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.test.factories import ServiceFactory

from woo_publications.utils.tests.vcr import VCRMixin

DUMMY_DOCUMENT_TYPE = (
    "http://host.docker.internal:8000"
    "/catalogi/api/v1/informatieobjecttypen/b3ff3b25-42eb-4e56-a587-ac632b286496"
)


class DocumentsApiIntegrationTests(VCRMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.documents_api_service = ServiceFactory.create(
            label="Open Zaak (docker-compose)",
            api_root="http://openzaak.docker.internal:8001/documenten/api/v1/",
            api_type=APITypes.drc,
            auth_type=AuthTypes.zgw,
            client_id="woo-publications-dev",
            secret="insecure-yQL9Rzh4eHGVmYx5w3J2gu",
        )

    def test_can_create_document_with_woo_publications_informatieobjecttype(self):
        client = build_client(self.documents_api_service)
        document_data = {
            "informatieobjecttype": DUMMY_DOCUMENT_TYPE,
            "bronorganisatie": "000000000",
            "creatiedatum": "2024-09-18",
            "titel": "Test document",
            "auteur": "Automated test suite",
            "taal": "ENG",
            "bestandsomvang": 0,
        }

        response = client.post("enkelvoudiginformatieobjecten", json=document_data)

        self.assertEqual(response.status_code, 201, response.json())
