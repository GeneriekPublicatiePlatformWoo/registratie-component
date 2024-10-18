from django.urls import reverse

from django_webtest import WebTest
from freezegun import freeze_time
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.publications.admin import PublicationAdmin
from woo_publications.publications.models import Document, Publication
from woo_publications.publications.tests.factories import (
    DocumentFactory,
    PublicationFactory,
)

from ..models import TimelineLogProxy


@disable_admin_mfa()
class TestAdminAuditLogging(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(
            is_staff=True,
            is_superuser=True,
        )

    @freeze_time("2024-09-25T00:14:00-00:00")
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

        form.submit(name="_save")

        added_item = Publication.objects.order_by("-pk").first()
        assert added_item is not None
        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "create",
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "object_data": {
                "uuid": str(added_item.uuid),
                "omschrijving": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur.",
                "verkorte_titel": "The title",
                "officiele_titel": "The official title of this publication",
                "registratiedatum": "2024-09-25T00:14:00Z",
            },
            "_cached_object_repr": "The official title of this publication",
        }

        self.assertEqual(log.extra_data, expected_data)

    @freeze_time("2024-09-27T00:14:00-00:00")
    def test_admin_update(self):
        assert not TimelineLogProxy.objects.exists()

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

        with self.subTest("read audit logging"):
            log = TimelineLogProxy.objects.first()
            assert log is not None

            expected_data = {
                "event": "read",
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "title one",
            }

            self.assertEqual(log.extra_data, expected_data)

        with self.subTest("update audit logging"):
            log = TimelineLogProxy.objects.last()
            assert log is not None

            expected_data = {
                "event": "update",
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "uuid": str(publication.uuid),
                    "omschrijving": "changed description",
                    "verkorte_titel": "changed short title",
                    "officiele_titel": "changed official title",
                    "registratiedatum": "2024-09-27T00:14:00Z",
                },
                "_cached_object_repr": "changed official title",
            }

            self.assertEqual(log.extra_data, expected_data)

    def test_admin_delete(self):
        assert not TimelineLogProxy.objects.exists()

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

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": "delete",
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "_cached_object_repr": "title one",
        }

        self.assertEqual(log.extra_data, expected_data)

    @freeze_time("2024-09-25T00:14:00-00:00")
    def test_admin_inline_update_admin(self):
        assert not TimelineLogProxy.objects.exists()

        publication = PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        document = DocumentFactory.create(
            publicatie=publication,
        )
        reverse_url = reverse(
            "admin:publications_publication_change",
            kwargs={"object_id": publication.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        with self.subTest("read audit logging"):
            log = TimelineLogProxy.objects.first()
            assert log is not None

            expected_data = {
                "event": "read",
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
            log = TimelineLogProxy.objects.filter(object_id=document.pk).first()
            assert log is not None

            expected_data = {
                "event": "create",
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "identifier": "http://example.com/1",
                    "publicatie": publication.id,
                    "bestandsnaam": "unknown.bin",
                    "creatiedatum": "2024-10-17",
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

    @freeze_time("2024-09-25T00:14:00-00:00")
    def test_admin_inline_create_admin(self):
        PublicationAdmin.inlines[0].extra = 1
        assert not TimelineLogProxy.objects.exists()
        assert not Document.objects.exists()

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
            log = TimelineLogProxy.objects.first()
            assert log is not None

            expected_data = {
                "event": "read",
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
            document = Document.objects.first()
            assert document is not None
            log = TimelineLogProxy.objects.filter(object_id=document.pk).first()
            assert log is not None

            expected_data = {
                "event": "create",
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "object_data": {
                    "identifier": "http://example.com/1",
                    "publicatie": publication.id,
                    "bestandsnaam": "unknown.bin",
                    "creatiedatum": "2024-10-17",
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
