import uuid

from django.urls import reverse

from django_webtest import WebTest
from freezegun import freeze_time
from maykin_2fa.test import disable_admin_mfa
from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.test.factories import ServiceFactory

from woo_publications.accounts.tests.factories import UserFactory

from ..models import Document
from .factories import DocumentFactory, PublicationFactory


@disable_admin_mfa()
class TestDocumentAdmin(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(
            is_staff=True,
            is_superuser=True,
        )

    def test_document_admin_shows_items(self):
        DocumentFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        DocumentFactory.create(
            officiele_titel="title two",
            verkorte_titel="two",
            omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
        )

        response = self.app.get(
            reverse("admin:publications_document_changelist"),
            user=self.user,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "field-identifier", 2)

    def test_document_admin_search(self):
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = DocumentFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = DocumentFactory.create(
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
        reverse_url = reverse("admin:publications_document_changelist")

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["changelist-search"]

        with self.subTest("filter_on_identifier"):
            form["q"] = publication.identifier

            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-identifier", 1)
            # searchbar + object
            self.assertContains(search_response, publication.identifier)
            self.assertNotContains(search_response, publication2.identifier)

        with self.subTest("filter_on_officiele_title"):
            form["q"] = "title one"
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, publication.identifier, 1)

        with self.subTest("filter_on_verkorte_titel"):
            form["q"] = "two"
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, publication2.identifier, 1)

        with self.subTest("filter_on_verkorte_titel"):
            form["q"] = str(publication.identifier)
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, "title one", 1)

        with freeze_time("2024-09-25T00:14:00-00:00"):
            with self.subTest("filter_on_registratiedatum"):
                today = "2024-09-25T00:00:00-00:00"
                tomorrow = "2024-09-26T00:00:00-00:00"

                search_response = self.app.get(
                    reverse_url,
                    {
                        "registratiedatum__gte": today,
                        "registratiedatum__lt": tomorrow,
                    },
                    user=self.user,
                )

                self.assertEqual(search_response.status_code, 200)
                self.assertContains(search_response, "field-identifier", 1)
                self.assertContains(search_response, publication2.identifier, 1)

    @freeze_time("2024-09-24T12:00:00-00:00")
    def test_document_admin_create(self):
        publication = PublicationFactory.create()
        identifier = f"https://www.openzaak.nl/documenten/{str(uuid.uuid4())}"

        response = self.app.get(
            reverse("admin:publications_document_add"),
            user=self.user,
        )

        self.assertEqual(response.status_code, 200)

        form = response.forms["document_form"]
        form["publicatie"] = publication.id
        form["identifier"] = identifier
        form["officiele_titel"] = "The official title of this document"
        form["verkorte_titel"] = "The title"
        form["creatiedatum"] = "2024-01-01"
        form["omschrijving"] = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
            "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur."
        )

        add_response = form.submit(name="_save")

        self.assertRedirects(
            add_response, reverse("admin:publications_document_changelist")
        )
        added_item = Document.objects.order_by("-pk").first()
        assert added_item is not None
        self.assertEqual(added_item.publicatie, publication)
        self.assertEqual(added_item.identifier, identifier)
        self.assertEqual(
            added_item.officiele_titel, "The official title of this document"
        )
        self.assertEqual(added_item.verkorte_titel, "The title")
        self.assertEqual(
            added_item.omschrijving,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
            "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur.",
        )
        self.assertEqual(str(added_item.registratiedatum), "2024-09-24 12:00:00+00:00")

    def test_document_admin_update(self):
        with freeze_time("2024-09-25T00:14:00-00:00"):
            document = DocumentFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        publication = PublicationFactory.create()
        identifier = f"https://www.openzaak.nl/documenten/{str(uuid.uuid4())}"
        reverse_url = reverse(
            "admin:publications_document_change",
            kwargs={"object_id": document.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["document_form"]
        form["publicatie"] = publication.id
        form["identifier"] = identifier
        form["officiele_titel"] = "changed official title"
        form["verkorte_titel"] = "changed short title"
        form["omschrijving"] = "changed description"

        response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)

        document.refresh_from_db()
        self.assertEqual(document.publicatie, publication)
        self.assertEqual(document.identifier, identifier)
        self.assertEqual(document.officiele_titel, "changed official title")
        self.assertEqual(document.verkorte_titel, "changed short title")
        self.assertEqual(document.omschrijving, "changed description")

    def test_publications_admin_delete(self):
        document = DocumentFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        reverse_url = reverse(
            "admin:publications_document_delete",
            kwargs={"object_id": document.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms[1]

        response = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Document.objects.filter(identifier=document.identifier).exists()
        )

    def test_document_admin_document_api_configuration(self):
        publication = PublicationFactory.create()
        service = ServiceFactory(
            api_root="https://example.com/",
            api_type=APITypes.drc,
            oas="https://example.com/api/v1/oas",
            header_key="Authorization",
            header_value="Token 0cbccf9e-f9cd-4f9c-9516-7481e79989df",
            auth_type=AuthTypes.api_key,
        )

        response = self.app.get(
            reverse("admin:publications_document_add"),
            user=self.user,
        )

        self.assertEqual(response.status_code, 200)

        with self.subTest("select box only shows document api options"):
            zaak_service = ServiceFactory(
                api_root="https://foo.com/",
                api_type=APITypes.zrc,
                oas="https://foo.com/api/v1/oas",
                header_key="Authorization",
                header_value="Token eef8d572-5fac-415c-9b8d-132b4b5eab19",
                auth_type=AuthTypes.api_key,
            )
            form = response.forms["document_form"]
            document_select = form["document_service"]

            self.assertEqual(len(document_select.options), 2)

            # test that default and document service are selectable but the zaak service isn't
            document_select.select(text="---------")
            document_select.select(text=str(service))
            with self.assertRaises(ValueError):
                document_select.select(text=str(zaak_service))

        with self.subTest(
            "provided both service and uuid configured creates item with no errors"
        ):
            form = response.forms["document_form"]
            form["publicatie"] = publication.id
            form["document_service"].select(text=str(service))
            form["document_uuid"] = uuid.uuid4()
            form["identifier"] = uuid.uuid4()
            form["officiele_titel"] = "The official title of this document"
            form["creatiedatum"] = "2024-01-01"

            add_response = form.submit(name="_save")

            self.assertRedirects(
                add_response, reverse("admin:publications_document_changelist")
            )
            added_item = Document.objects.order_by("-pk").first()
            assert added_item is not None

        with self.subTest(
            "provided no service and uuid configured creates item with no errors"
        ):
            form = response.forms["document_form"]
            form["publicatie"] = publication.id
            form["document_service"].select(text="---------")
            form["document_uuid"] = ""
            form["identifier"] = uuid.uuid4()
            form["officiele_titel"] = "The official title of this document"
            form["creatiedatum"] = "2024-01-01"

            add_response = form.submit(name="_save")

            self.assertRedirects(
                add_response, reverse("admin:publications_document_changelist")
            )
            added_item = Document.objects.order_by("-pk").first()
            assert added_item is not None

        with self.subTest(
            "provided only service and no uuid configured results in error"
        ):
            form = response.forms["document_form"]
            form["publicatie"] = publication.id
            form["document_service"].select(text=str(service))
            form["document_uuid"] = ""
            form["identifier"] = uuid.uuid4()
            form["officiele_titel"] = "The official title of this document"
            form["creatiedatum"] = "2024-01-01"

            add_response = form.submit(name="_save")

            self.assertEqual(add_response.status_code, 200)
            self.assertContains(
                add_response,
                "You must specify both the Document API Service "
                "and Document UUID to identify a document.",
            )

        with self.subTest(
            "provided only uuid and no service configured results in error"
        ):
            form = response.forms["document_form"]
            form["publicatie"] = publication.id
            form["document_service"].select(text="---------")
            form["document_uuid"] = uuid.uuid4()
            form["identifier"] = uuid.uuid4()
            form["officiele_titel"] = "The official title of this document"
            form["creatiedatum"] = "2024-01-01"

            add_response = form.submit(name="_save")

            self.assertEqual(add_response.status_code, 200)
            self.assertContains(
                add_response,
                "You must specify both the Document API Service "
                "and Document UUID to identify a document.",
            )
