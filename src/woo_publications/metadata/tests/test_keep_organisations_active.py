from django.test import TestCase

from ..keep_organisations_active import keep_organisations_active
from ..models import Organisation
from .factories import OrganisationFactory


class KeepOrganisationsActiveTests(TestCase):
    def test_active_organisations_updated_orgs_stay_active(self):
        assert not Organisation.objects.exists()
        organisation, organisation2, organisation3 = OrganisationFactory.create_batch(
            3, is_actief=True
        )

        with keep_organisations_active():
            Organisation.objects.update(is_actief=False)

        organisation.refresh_from_db()
        organisation2.refresh_from_db()
        organisation3.refresh_from_db()

        self.assertTrue(organisation.is_actief)
        self.assertTrue(organisation2.is_actief)
        self.assertTrue(organisation3.is_actief)

    def test_inactive_organisations_are_still_inactive(self):
        assert not Organisation.objects.exists()
        organisation, organisation2, organisation3 = OrganisationFactory.create_batch(
            3, is_actief=False
        )

        with keep_organisations_active():
            pass

        organisation.refresh_from_db()
        organisation2.refresh_from_db()
        organisation3.refresh_from_db()

        self.assertFalse(organisation.is_actief)
        self.assertFalse(organisation2.is_actief)
        self.assertFalse(organisation3.is_actief)
