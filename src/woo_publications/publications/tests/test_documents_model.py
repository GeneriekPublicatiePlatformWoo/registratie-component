import uuid

from django.db import IntegrityError, transaction
from django.test import TestCase

from zgw_consumers.constants import APITypes
from zgw_consumers.test.factories import ServiceFactory

from .factories import DocumentFactory


class TestDocumentApi(TestCase):
    def test_document_api_constraint(self):
        service = ServiceFactory.create(
            api_root="https://example.com/",
            api_type=APITypes.drc,
        )

        with self.subTest(
            "provided both service and uuid configured creates item with no errors"
        ):
            document = DocumentFactory.create(
                document_service=service, document_uuid=uuid.uuid4()
            )
            self.assertIsNotNone(document.pk)

        with self.subTest(
            "provided no service and uuid configured creates item with no errors"
        ):
            document = DocumentFactory.create(document_service=None, document_uuid=None)
            self.assertIsNotNone(document.pk)

        with (
            self.subTest(
                "provided only service and no uuid configured results in error"
            ),
            self.assertRaises(IntegrityError),
            transaction.atomic(),
        ):
            DocumentFactory.create(document_service=service, document_uuid=None)

        with (
            self.subTest(
                "provided only uuid and no service configured results in error"
            ),
            self.assertRaises(IntegrityError),
            transaction.atomic(),
        ):
            DocumentFactory.create(document_service=None, document_uuid=uuid.uuid4())
