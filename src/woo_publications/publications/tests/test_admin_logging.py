from django.urls import reverse

from django_webtest import WebTest
from freezegun import freeze_time
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy
from woo_publications.utils.tests.webtest import add_dynamic_field

from ..models import Document, Publication
from .factories import DocumentFactory, PublicationFactory


@disable_admin_mfa()
class TestAdminAuditLogging(WebTest):
    """
    Test that CRUD actions on publications are audit-logged.

    We have a generic implementation in woo_publications.logging for this behaviour,
    for which the code coverage is provided through this test class.

    Additionally, there's a system check to ensure audit logging is added to our admin
    classes, which should cover the rest of the apps/models.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(superuser=True)

    def test_admin_create(self):
        assert not TimelineLogProxy.objects.exists()
        reverse_url = reverse("admin:publications_publication_add")

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["publication_form"]
        form["officiele_titel"] = "The official title of this publication"
        form["verkorte_titel"] = "The title"
        form["omschrijving"] = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
            "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur."
        )

        with freeze_time("2024-09-25T00:14:00-00:00"):
            form.submit(name="_save")

        added_item = Publication.objects.get()
        log = TimelineLogProxy.objects.get()

        expected_data = {
            "event": Events.create,
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "object_data": {
                "id": added_item.pk,
                "uuid": str(added_item.uuid),
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur.",
                "verkorte_titel": "The title",
                "officiele_titel": "The official title of this publication",
                "registratiedatum": "2024-09-25T00:14:00Z",
            },
            "_cached_object_repr": "The official title of this publication",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_admin_update(self):
        assert not TimelineLogProxy.objects.exists()
        with freeze_time("2024-09-27T00:14:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        reverse_url = reverse(
            "admin:publications_publication_change",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["publication_form"]
        form["officiele_titel"] = "changed official title"
        form["verkorte_titel"] = "changed short title"
        form["omschrijving"] = "changed description"

        form.submit(name="_save")

        publication.refresh_from_db()

        self.assertEqual(TimelineLogProxy.objects.count(), 2)
        read_log, update_log = TimelineLogProxy.objects.order_by("pk")

        with self.subTest("read audit logging"):
            expected_data = {
                "event": Events.read,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "title one",
            }

            self.assertEqual(read_log.extra_data, expected_data)

        with self.subTest("update audit logging"):
            expected_data = {
                "event": Events.update,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "id": publication.pk,
                    "uuid": str(publication.uuid),
                    "omschrijving": "changed description",
                    "verkorte_titel": "changed short title",
                    "officiele_titel": "changed official title",
                    "registratiedatum": "2024-09-27T00:14:00Z",
                },
                "_cached_object_repr": "changed official title",
            }

            self.assertEqual(update_log.extra_data, expected_data)

    def test_admin_delete(self):
        assert not TimelineLogProxy.objects.exists()

        with freeze_time("2024-09-27T00:14:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        reverse_url = reverse(
            "admin:publications_publication_delete",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms[1]
        response = form.submit()

        self.assertEqual(response.status_code, 302)

        log = TimelineLogProxy.objects.get()

        expected_data = {
            "event": Events.delete,
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "object_data": {
                "id": publication.pk,
                "uuid": str(publication.uuid),
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "verkorte_titel": "one",
                "officiele_titel": "title one",
                "registratiedatum": "2024-09-27T00:14:00Z",
            },
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_admin_inline_update_admin(self):
        assert not TimelineLogProxy.objects.exists()

        with freeze_time("2024-09-25T00:14:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
            document = DocumentFactory.create(publicatie=publication)
        reverse_url = reverse(
            "admin:publications_publication_change",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        with self.subTest("read audit logging"):
            log = TimelineLogProxy.objects.get()

            expected_data = {
                "event": Events.read,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "title one",
            }

            self.assertEqual(log.extra_data, expected_data)

        form = response.forms["publication_form"]
        form["document_set-0-identifier"] = "http://example.com/1"
        form["document_set-0-officiele_titel"] = "title"
        form["document_set-0-creatiedatum"] = "17-10-2024"
        response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)

        with self.subTest("update inline update logging"):
            log = TimelineLogProxy.objects.filter(object_id=str(document.pk)).first()
            assert log is not None

            expected_data = {
                "event": Events.update,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "id": document.pk,
                    "uuid": str(document.uuid),
                    "identifier": "http://example.com/1",
                    "publicatie": publication.id,
                    "bestandsnaam": "unknown.bin",
                    "creatiedatum": "2024-10-17",
                    "document_service": None,
                    "document_uuid": None,
                    "omschrijving": "",
                    "bestandsomvang": 0,
                    "verkorte_titel": "",
                    "bestandsformaat": "unknown",
                    "officiele_titel": "title",
                    "registratiedatum": "2024-09-25T00:14:00Z",
                },
                "_cached_object_repr": "title",
            }

            self.assertEqual(log.extra_data, expected_data)

    def test_admin_inline_create_admin(self):
        assert not TimelineLogProxy.objects.exists()
        assert not Document.objects.exists()

        with freeze_time("2024-09-25T00:14:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        reverse_url = reverse(
            "admin:publications_publication_change",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        with self.subTest("read audit logging"):
            log = TimelineLogProxy.objects.get()

            expected_data = {
                "event": Events.read,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "title one",
            }

            self.assertEqual(log.extra_data, expected_data)

        form = response.forms["publication_form"]

        form["document_set-TOTAL_FORMS"] = "1"  # we're adding one, dynamically
        add_dynamic_field(form, "document_set-0-identifier", "http://example.com/1")
        add_dynamic_field(form, "document_set-0-officiele_titel", "title")
        add_dynamic_field(form, "document_set-0-creatiedatum", "17-10-2024")
        add_dynamic_field(form, "document_set-0-bestandsformaat", "application/pdf")
        add_dynamic_field(form, "document_set-0-bestandsnaam", "foo.pdf")
        add_dynamic_field(form, "document_set-0-bestandsomvang", "0")

        with freeze_time("2024-09-26T00:14:00-00:00"):
            response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)

        with self.subTest("update inline update logging"):
            document = Document.objects.get()
            log = TimelineLogProxy.objects.filter(
                object_id=str(document.pk), extra_data___cached_object_repr="title"
            ).get()

            expected_data = {
                "event": Events.create,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "id": document.pk,
                    "uuid": str(document.uuid),
                    "identifier": "http://example.com/1",
                    "publicatie": publication.id,
                    "bestandsnaam": "foo.pdf",
                    "creatiedatum": "2024-10-17",
                    "document_service": None,
                    "document_uuid": None,
                    "omschrijving": "",
                    "bestandsomvang": 0,
                    "verkorte_titel": "",
                    "bestandsformaat": "application/pdf",
                    "officiele_titel": "title",
                    "registratiedatum": "2024-09-26T00:14:00Z",
                },
                "_cached_object_repr": "title",
            }

            self.assertEqual(log.extra_data, expected_data)

    def test_admin_inline_delete(self):
        assert not TimelineLogProxy.objects.exists()

        with freeze_time("2024-09-25T00:14:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
            document = DocumentFactory.create(
                publicatie=publication,
                identifier="document-1",
                officiele_titel="DELETE THIS ITEM",
                verkorte_titel="",
                omschrijving="",
                creatiedatum="2024-09-25",
            )
        reverse_url = reverse(
            "admin:publications_publication_change",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        with self.subTest("read audit logging"):
            log = TimelineLogProxy.objects.get()

            expected_data = {
                "event": Events.read,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "title one",
            }

            self.assertEqual(log.extra_data, expected_data)

        form = response.forms["publication_form"]
        form["document_set-0-DELETE"] = True
        response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)

        with self.subTest("update inline update logging"):
            log = TimelineLogProxy.objects.filter(
                object_id=str(document.pk),
                extra_data___cached_object_repr="DELETE THIS ITEM",
            ).first()
            assert log is not None

            expected_data = {
                "event": Events.delete.value,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "id": document.pk,
                    "identifier": "document-1",
                    "publicatie": publication.id,
                    "bestandsnaam": "unknown.bin",
                    "creatiedatum": "2024-09-25",
                    "omschrijving": "",
                    "document_uuid": None,
                    "bestandsomvang": 0,
                    "verkorte_titel": "",
                    "bestandsformaat": "unknown",
                    "officiele_titel": "DELETE THIS ITEM",
                    "document_service": None,
                    "registratiedatum": "2024-09-25T00:14:00Z",
                },
                "_cached_object_repr": "DELETE THIS ITEM",
            }

            self.assertEqual(log.extra_data, expected_data)
