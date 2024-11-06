"""
Configuration admin (smoke)tests.
"""

from django.urls import reverse

from django_webtest import WebTest
from maykin_2fa.test import disable_admin_mfa

from woo_publications.accounts.tests.factories import UserFactory

from ..models import GlobalConfiguration


@disable_admin_mfa()
class SmokeTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(superuser=True)

    def setUp(self):
        super().setUp()
        self.addCleanup(GlobalConfiguration.clear_cache)

    def test_initial_config_creation_does_not_crash(self):
        assert not GlobalConfiguration.objects.exists(), "Expected no config to exist"
        url = reverse("admin:config_globalconfiguration_change", args=(1,))

        self.app.get(url, user=self.user)

        self.assertTrue(
            GlobalConfiguration.objects.exists(),
            "Expected the configuration instance to be created",
        )
