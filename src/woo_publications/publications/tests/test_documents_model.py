import uuid

from django.db import IntegrityError, transaction
from django.test import TestCase

from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.test.factories import ServiceFactory

from ..models import Document
from .factories import PublicationFactory


class TestDocumentApi(TestCase):
    def test_document_api_constraint(self):
        assert not Document.objects.exists()
        publication = PublicationFactory.create()
        service = ServiceFactory(
            api_root="https://example.com/",
            api_type=APITypes.drc,
            oas="https://example.com/api/v1/oas",
            header_key="Authorization",
            header_value="Token 0cbccf9e-f9cd-4f9c-9516-7481e79989df",
            auth_type=AuthTypes.api_key,
        )

        with self.subTest(
            "provided both service and uuid configured creates item with no errors"
        ):
            document = Document.objects.create(
                publicatie=publication,
                document_service=service,
                document_uuid=uuid.uuid4(),
                identifier=uuid.uuid4(),
                officiele_titel="Document with service and uuid configured gets created.",
                creatiedatum="2024-01-01",
            )
            self.assertIsNotNone(document.pk)

        with self.subTest(
            "provided no service and uuid configured creates item with no errors"
        ):
            document = Document.objects.create(
                publicatie=publication,
                identifier=uuid.uuid4(),
                officiele_titel="Document without service and uuid configured gets created.",
                creatiedatum="2024-01-01",
            )
            self.assertIsNotNone(document.pk)

        with self.subTest(
            "provided only service and no uuid configured results in error"
        ):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Document.objects.create(
                    publicatie=publication,
                    document_service=service,
                    identifier=uuid.uuid4(),
                    officiele_titel="Document with service and without uuid configured raises error.",
                    creatiedatum="2024-01-01",
                )

        with self.subTest(
            "provided only uuid and no service configured results in error"
        ):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Document.objects.create(
                    publicatie=publication,
                    document_uuid=uuid.uuid4(),
                    identifier=uuid.uuid4(),
                    officiele_titel="Document with uuid and without service configured raises error.",
                    creatiedatum="2024-01-01",
                )
