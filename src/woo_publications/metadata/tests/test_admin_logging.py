from django.urls import reverse

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy

from ..constants import OrganisationOrigins
from ..models import Organisation
from .factories import OrganisationFactory


@disable_admin_mfa()
class TestOrganisationAdminAuditLogging(WebTest):
    """
    Test that CRUD actions on organisations are audit-logged.

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
        reverse_url = reverse("admin:metadata_organisation_add")

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["organisation_form"]
        form["naam"] = "organisation name"

        form.submit(name="_save")

        added_item = Organisation.objects.order_by("-pk").first()
        assert added_item is not None
        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": Events.create,
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "object_data": {
                "id": added_item.pk,
                "uuid": str(added_item.uuid),
                "identifier": added_item.identifier,
                "naam": "organisation name",
                "oorsprong": OrganisationOrigins.custom_entry,
                "is_actief": True,
            },
            "_cached_object_repr": "organisation name",
        }

        self.assertEqual(log.extra_data, expected_data)

    def test_admin_update(self):
        assert not TimelineLogProxy.objects.exists()
        organisation = OrganisationFactory.create(
            naam="organisation name",
        )
        reverse_url = reverse(
            "admin:metadata_organisation_change",
            kwargs={"object_id": organisation.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms["organisation_form"]
        form["naam"] = "changed name"
        form["is_actief"] = False

        form.submit(name="_save")

        organisation.refresh_from_db()

        self.assertEqual(TimelineLogProxy.objects.count(), 2)
        read_log, update_log = TimelineLogProxy.objects.order_by("pk")

        with self.subTest("read audit logging"):
            expected_data = {
                "event": Events.read,
                "acting_user": {
                    "identifier": self.user.id,
                    "display_name": self.user.get_full_name(),
                },
                "_cached_object_repr": "organisation name",
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
                    "id": organisation.pk,
                    "uuid": str(organisation.uuid),
                    "identifier": organisation.identifier,
                    "naam": "changed name",
                    "oorsprong": OrganisationOrigins.custom_entry,
                    "is_actief": False,
                },
                "_cached_object_repr": "changed name",
            }

            self.assertEqual(update_log.extra_data, expected_data)

    def test_admin_delete(self):
        assert not TimelineLogProxy.objects.exists()

        organisation = OrganisationFactory.create(
            naam="soon to be deleted organisation",
        )
        reverse_url = reverse(
            "admin:metadata_organisation_delete",
            kwargs={"object_id": organisation.id},
        )

        response = self.app.get(reverse_url, user=self.user)

        self.assertEqual(response.status_code, 200)

        form = response.forms[1]
        response = form.submit()

        self.assertEqual(response.status_code, 302)

        log = TimelineLogProxy.objects.first()
        assert log is not None

        expected_data = {
            "event": Events.delete,
            "acting_user": {
                "identifier": self.user.id,
                "display_name": self.user.get_full_name(),
            },
            "object_data": {
                "id": organisation.pk,
                "uuid": str(organisation.uuid),
                "identifier": organisation.identifier,
                "naam": "soon to be deleted organisation",
                "oorsprong": OrganisationOrigins.custom_entry,
                "is_actief": True,
            },
            "_cached_object_repr": "soon to be deleted organisation",
        }

        self.assertEqual(log.extra_data, expected_data)
