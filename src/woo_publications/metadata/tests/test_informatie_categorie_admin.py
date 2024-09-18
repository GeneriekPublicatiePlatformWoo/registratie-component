from django.urls import reverse

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.metadata.constants import InformatieCategorieOrigins
from woo_publications.metadata.models import InformatieCategorie
from woo_publications.metadata.tests.factories import InformatieCategorieFactory


@disable_admin_mfa()
class TestInformatieCategorieAdmin(WebTest):
    def setUp(self):
        self.user = UserFactory.create(
            is_staff=True,
            is_superuser=True,
        )
        self.information_category_value_list = InformatieCategorieFactory.create(
            identifier="https://www.example.com/waardenlijsten/1",
            naam="first item",
            order=0,
            oorsprong=InformatieCategorieOrigins.value_list,
        )
        self.information_category_custom_entry = InformatieCategorieFactory.create(
            identifier="https://www.example.com/waardenlijsten/2",
            naam="second item",
            order=1,
            oorsprong=InformatieCategorieOrigins.custom_entry,
        )
        super().setUp()

    def test_informatie_category_admin_show_items(self):
        response = self.app.get(
            reverse(
                "admin:metadata_informatiecategorie_changelist",
            ),
            user=self.user,
        )

        self.assertEqual(response.status_int, 200)
        # first item
        self.assertInHTML(
            "https://www.example.com/waardenlijsten/1",
            str(response.content),
        )
        self.assertInHTML(
            '<td class="field-naam">first item</td>',
            str(response.content),
        )
        self.assertInHTML('<td class="field-order">0</td>', str(response.content))

        # second item
        self.assertInHTML(
            "https://www.example.com/waardenlijsten/2",
            str(response.content),
        )
        self.assertInHTML(
            '<td class="field-naam">second item</td>',
            str(response.content),
        )
        self.assertInHTML('<td class="field-order">1</td>', str(response.content))

    def test_informatie_category_admin_show_item_search(self):
        url = reverse("admin:metadata_informatiecategorie_changelist")

        with self.subTest("filter_on_naam"):
            response = self.app.get(url, {"q": "first item"}, user=self.user)

            self.assertEqual(response.status_int, 200)
            # first item in list
            self.assertInHTML(
                '<td class="field-naam">first item</td>',
                str(response.content),
            )
            # second item not in list
            with self.assertRaises(AssertionError):
                self.assertInHTML(
                    '<td class="field-naam">second item</td>',
                    str(response.content),
                )

        with self.subTest("filter_on_identifier"):
            response = self.app.get(
                url, {"q": "https://www.example.com/waardenlijsten/2"}, user=self.user
            )

            self.assertEqual(response.status_int, 200)
            # first item in list
            self.assertInHTML(
                "https://www.example.com/waardenlijsten/2",
                str(response.content),
            )
            # second item not in list
            with self.assertRaises(AssertionError):
                self.assertInHTML(
                    "https://www.example.com/waardenlijsten/1",
                    str(response.content),
                )

        with self.subTest("filter_on_oorsprong"):
            response = self.app.get(
                url,
                {"oorsprong__exact": InformatieCategorieOrigins.value_list},
                user=self.user,
            )

            self.assertEqual(response.status_int, 200)
            # first item in list
            self.assertInHTML(
                "https://www.example.com/waardenlijsten/1",
                str(response.content),
            )
            # second item not in list
            with self.assertRaises(AssertionError):
                self.assertInHTML(
                    "https://www.example.com/waardenlijsten/2",
                    str(response.content),
                )

    def test_informatie_category_admin_can_not_update_item_with_oorsprong_waardenlijst(
        self,
    ):
        url = reverse(
            "admin:metadata_informatiecategorie_change",
            kwargs={"object_id": self.information_category_value_list.id},
        )

        response = self.app.get(url, user=self.user)
        form = response.forms["informatiecategorie_form"]

        self.assertEqual(response.status_code, 200)
        # page doesn't have save button.
        with self.assertRaisesMessage(
            AssertionError,
            'Couldn\'t find \'<input class="default" name="_save" type="submit" value="Opslaan">\' in response',
        ):
            self.assertInHTML(
                '<input type="submit" value="Opslaan" class="default" name="_save">',
                str(response.content),
            )

        with self.assertRaisesMessage(
            AssertionError,
            "No field by the name 'identifier' found (fields: 'csrfmiddlewaretoken')",
        ):
            form["identifier"] = "https://www.example.com/waardenlijsten/12"

    def test_informatie_category_admin_can_update_item_with_oorsprong_zelf_toegevoegd(
        self,
    ):
        url = reverse(
            "admin:metadata_informatiecategorie_change",
            kwargs={"object_id": self.information_category_custom_entry.id},
        )

        response = self.app.get(url, user=self.user)
        form = response.forms["informatiecategorie_form"]

        self.assertEqual(response.status_code, 200)
        # page has save button.
        self.assertInHTML(
            '<input type="submit" value="Opslaan" class="default" name="_save">',
            str(response.content),
        )

        # test if identifier isn't editable
        with self.assertRaises(AssertionError):
            form["identifier"] = "https://www.example.com/waardenlijsten/12"

        form["naam"] = "changed"
        form["naam_meervoud"] = "changed"
        form["definitie"] = "changed"
        response = form.submit("submit")

        self.assertEqual(response.status_code, 302)
        self.information_category_custom_entry.refresh_from_db()

        self.assertEqual(self.information_category_custom_entry.naam, "changed")
        self.assertEqual(
            self.information_category_custom_entry.naam_meervoud, "changed"
        )
        self.assertEqual(self.information_category_custom_entry.definitie, "changed")

    def test_informatie_category_admin_create_item(self):
        response = self.app.get(
            reverse("admin:metadata_informatiecategorie_add"), user=self.user
        )
        form = response.forms["informatiecategorie_form"]

        form["identifier"] = "https://www.example.com/waardenlijsten/999"
        form["naam"] = "new item"
        form["naam_meervoud"] = "new items"
        form["definitie"] = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
            "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur."
        )

        form.submit("submit")
        self.assertTrue(
            InformatieCategorie.objects.filter(
                identifier="https://www.example.com/waardenlijsten/999",
                naam="new item",
                naam_meervoud="new items",
                definitie=(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris risus nibh, "
                    "iaculis eu cursus sit amet, accumsan ac urna. Mauris interdum eleifend eros sed consectetur."
                ),
                oorsprong=InformatieCategorieOrigins.custom_entry,
                order=2,
            ).exists()
        )
