from django.urls import reverse

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory

from ..constants import OrganisationOrigins
from ..models import CUSTOM_ORGANISATION_URL_PREFIX, Organisation
from .factories import OrganisationFactory


@disable_admin_mfa()
class TestOrganisationAdmin(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(
            is_staff=True,
            is_superuser=True,
        )

    def test_organisation_admin_show_items(self):
        OrganisationFactory.create(
            naam="first item",
            oorsprong=OrganisationOrigins.municipality_list,
            is_actief=True,
        )
        OrganisationFactory.create(
            naam="second item",
            oorsprong=OrganisationOrigins.custom_entry,
            is_actief=True,
        )
        response = self.app.get(
            reverse(
                "admin:metadata_organisation_changelist",
            ),
            user=self.user,
        )

        self.assertEqual(response.status_code, 200)

        # test the amount of rows present
        self.assertContains(response, "field-identifier", 2)

    def test_organisation_admin_show_item_search(self):
        organisation = OrganisationFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            oorsprong=OrganisationOrigins.municipality_list,
            is_actief=True,
        )
        organisation2 = OrganisationFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            oorsprong=OrganisationOrigins.custom_entry,
            is_actief=False,
        )
        url = reverse("admin:metadata_organisation_changelist")

        response = self.app.get(url, user=self.user)

        form = response.forms["changelist-search"]

        with self.subTest("filter_on_naam"):
            form["q"] = "first item"
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)

            # test the amount of rows present
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, organisation.identifier, 1)

        with self.subTest("filter_on_identifier"):
            form["q"] = organisation2.identifier
            search_response = form.submit()

            self.assertEqual(search_response.status_code, 200)

            # test the amount of rows present
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, "second item", 1)

        with self.subTest("filter_on_oorsprong"):
            search_response = self.app.get(
                url,
                {"oorsprong__exact": OrganisationOrigins.municipality_list},
                user=self.user,
            )

            self.assertEqual(search_response.status_code, 200)

            # test the amount of rows present
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, organisation.identifier, 1)

        with self.subTest("filter_on_is_actief"):
            search_response = self.app.get(
                url,
                {"is_actief__exact": True},
                user=self.user,
            )

            self.assertEqual(search_response.status_code, 200)

            # test the amount of rows present
            self.assertContains(search_response, "field-identifier", 1)
            self.assertContains(search_response, organisation.identifier, 1)

    def test_organisation_admin_can_not_update_item_with_oorsprong_waardenlijst(
        self,
    ):
        organisation = OrganisationFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            oorsprong=OrganisationOrigins.municipality_list,
            is_actief=True,
        )
        url = reverse(
            "admin:metadata_organisation_change",
            kwargs={"object_id": organisation.id},
        )

        response = self.app.get(url, user=self.user)
        self.assertEqual(response.status_code, 200)

        form = response.forms["organisation_form"]
        self.assertNotIn("naam", form.fields)

    def test_organisation_admin_can_update_item_with_oorsprong_zelf_toegevoegd(
        self,
    ):
        organisation = OrganisationFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            oorsprong=OrganisationOrigins.custom_entry,
            is_actief=True,
        )
        url = reverse(
            "admin:metadata_organisation_change",
            kwargs={"object_id": organisation.id},
        )

        response = self.app.get(url, user=self.user)
        self.assertEqual(response.status_code, 200)

        form = response.forms["organisation_form"]
        self.assertIn("naam", form.fields)

        # test if identifier isn't editable
        self.assertNotIn("identifier", form.fields)

        form["naam"] = "changed"
        response = form.submit(name="_save")

        self.assertEqual(response.status_code, 302)
        organisation.refresh_from_db()

        self.assertEqual(organisation.naam, "changed")

    def test_organisation_admin_create_item(self):
        response = self.app.get(
            reverse("admin:metadata_organisation_add"), user=self.user
        )

        form = response.forms["organisation_form"]
        form["naam"] = "new item"

        form.submit(name="_save")

        added_item = Organisation.objects.order_by("-pk").first()
        assert added_item is not None
        self.assertEqual(added_item.naam, "new item")
        self.assertTrue(
            added_item.identifier.startswith(CUSTOM_ORGANISATION_URL_PREFIX)
        )
        self.assertTrue(added_item.is_actief)
        self.assertEqual(added_item.oorsprong, OrganisationOrigins.custom_entry)
