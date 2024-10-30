"""
Test the documents API client.

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
"""

from datetime import date
from uuid import uuid4

from django.test import TestCase

from woo_publications.utils.tests.vcr import VCRMixin

from ..client import get_client
from .factories import ServiceFactory

DOCUMENT_TYPE_URL = (
    "http://host.docker.internal:8000/catalogi/api/v1/informatieobjecttypen/"
    "9aeb7501-3f77-4f36-8c8f-d21f47c2d6e8"  # this UUID is in the fixture
)


class DocumentsAPIClientTests(VCRMixin, TestCase):

    def test_create_document_with_file_parts_upload(self):
        service = ServiceFactory.build(for_documents_api_docker_compose=True)
        client = get_client(service)

        document = client.create_document(
            identification=str(uuid4()),  # must be unique for the source organisation
            source_organisation="123456782",
            document_type_url=DOCUMENT_TYPE_URL,
            creation_date=date.today(),
            title="Sample document",
            filesize=256_000,  # in bytes
            filename="sample.png",
            content_type="image/png",
            description="a" * 5000,  # use a long string and try to break it
        )

        self.assertGreater(len(str(document.uuid)), 0)
        # we expect a lock to be returend
        self.assertIsInstance(document.lock, str)
        self.assertNotEqual(document.lock, "")

        # given the upload size & configuration of Open Zaak, we only expect one part
        self.assertEqual(len(parts := document.file_parts), 1)
        self.assertGreater(len(str(parts[0].uuid)), 0)
        self.assertEqual(parts[0].size, 256_000)

        with self.subTest("check document is created"):
            # and we expect that we can fetch the document too
            detail_response = client.get(
                f"enkelvoudiginformatieobjecten/{document.uuid}"
            )

            self.assertEqual(detail_response.status_code, 200)
