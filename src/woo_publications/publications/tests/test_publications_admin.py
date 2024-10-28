from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest
from freezegun import freeze_time
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory

from ..models import Publication
from .factories import PublicationFactory


@disable_admin_mfa()
class TestPublicationsAdmin(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(superuser=True)

    def test_publications_admin_shows_items(self):
        PublicationFactory.create(
            officiele_titel="title one",
            verkorte_titel="one",
            omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )
        PublicationFactory.create(
            officiele_titel="title two",
            verkorte_titel="two",
            omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
        )
        response = self.app.get(
            reverse("admin:publications_publication_changelist"),
            user=self.user,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "field-uuid", 2)

    def test_publications_admin_search(self):
        with freeze_time("2024-09-24T12:00:00-00:00"):
            publication = PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = PublicationFactory.create(
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
        reverse_url = reverse("admin:publications_publication_changelist")

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["changelist-search"]

        with self.subTest("filter_on_officiele_title"):
            form["q"] = "title one"
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-uuid", 1)
            self.assertContains(search_response, str(publication.uuid), 1)

        with self.subTest("filter_on_verkorte_titel"):
            form["q"] = "two"
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-uuid", 1)
            self.assertContains(search_response, str(publication2.uuid), 1)

        with self.subTest("filter_on_verkorte_titel"):
            form["q"] = str(publication.uuid)
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-uuid", 1)
            self.assertContains(search_response, "title one", 1)

    def test_publication_list_filter(self):
        self.app.set_user(user=self.user)

        with freeze_time("2024-09-24T12:00:00-00:00"):
            PublicationFactory.create(
                officiele_titel="title one",
                verkorte_titel="one",
                omschrijving="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            )
        with freeze_time("2024-09-25T12:30:00-00:00"):
            publication2 = PublicationFactory.create(
                officiele_titel="title two",
                verkorte_titel="two",
                omschrijving="Vestibulum eros nulla, tincidunt sed est non, facilisis mollis urna.",
            )
        reverse_url = reverse("admin:publications_publication_changelist")

        with freeze_time("2024-09-25T00:14:00-00:00"):
            response = self.app.get(reverse_url)

        self.assertEqual(response.status_code, 200)

        with self.subTest("filter_on_registratiedatum"):
            search_response = response.click(description=_("Today"), index=0)

            self.assertEqual(search_response.status_code, 200)

            # Sanity check that we indeed filtered on registratiedatum
            self.assertIn(
                "registratiedatum", search_response.request.environ["QUERY_STRING"]
            )

            self.assertEqual(search_response.status_code, 200)
            self.assertContains(search_response, "field-uuid", 1)
            self.assertContains(search_response, str(publication2.uuid), 1)

    @freeze_time("2024-09-25T00:14:00-00:00")
    def test_publications_admin_create(self):
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
        self.assertEqual(
            added_item.officiele_titel, "The official title of this publication"
        )
        self.assertEqual(added_item.verkorte_titel, "The title")
        self.assertEqual(
            added_item.omschrijving,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
            "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur.",
        )
        self.assertEqual(str(added_item.registratiedatum), "2024-09-25 00:14:00+00:00")

    def test_publications_admin_update(self):
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

        form = response.forms["publication_form"]
        form["officiele_titel"] = "changed official title"
        form["verkorte_titel"] = "changed short title"
        form["omschrijving"] = "changed description"

        with freeze_time("2024-09-27T00:14:00-00:00"):
            response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)

        publication.refresh_from_db()
        self.assertEqual(publication.officiele_titel, "changed official title")
        self.assertEqual(publication.verkorte_titel, "changed short title")
        self.assertEqual(publication.omschrijving, "changed description")
        self.assertEqual(str(publication.registratiedatum), "2024-09-25 00:14:00+00:00")

    def test_publications_admin_delete(self):
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
        self.assertFalse(Publication.objects.filter(uuid=publication.uuid).exists())
