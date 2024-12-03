from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from ..models import Organisation
from .factories import OrganisationFactory

organisation_fixture = Path(
    settings.DJANGO_PROJECT_DIR / "metadata" / "tests" / "organisations_fixture.json",
)


class LoadOrganisationsCommandTests(TestCase):
    def test_load_org_with_empty_db(self):
        assert not Organisation.objects.exists()

        call_command(
            "load_organisations",
            organisation_fixture,
            stdout=StringIO(),
        )

        self.assertEqual(Organisation.objects.count(), 5)

    def test_load_org_with_random_orgs(self):
        assert not Organisation.objects.exists()

        OrganisationFactory.create_batch(3)

        call_command(
            "load_organisations",
            organisation_fixture,
            stdout=StringIO(),
        )

        self.assertEqual(Organisation.objects.count(), 8)

    def test_load_updated_active_orgs_remain_active(self):
        assert not Organisation.objects.exists()

        organisation = OrganisationFactory.create(
            uuid="d74932b6-63ae-488f-97d1-63b176f61ad4",
            identifier="https://identifier.overheid.nl/tooi/id/so/so0006",
            is_actief=True,
        )
        organisation2 = OrganisationFactory.create(
            uuid="2010f12e-31c1-4a3d-81fb-03e0e7f21989",
            identifier="https://identifier.overheid.nl/tooi/id/so/so0011",
            is_actief=True,
        )

        call_command(
            "load_organisations",
            organisation_fixture,
            stdout=StringIO(),
        )

        organisation.refresh_from_db()
        organisation2.refresh_from_db()

        self.assertEqual(Organisation.objects.count(), 5)
        self.assertTrue(organisation.is_actief)
        self.assertTrue(organisation2.is_actief)

    def test_wrong_variable(self):
        with self.assertRaisesMessage(
            CommandError, "No fixture named 'not a file' found."
        ):
            call_command(
                "load_organisations",
                "not a file",
                stdout=StringIO(),
            )
