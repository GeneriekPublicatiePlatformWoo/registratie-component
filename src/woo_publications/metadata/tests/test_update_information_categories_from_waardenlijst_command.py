import tempfile

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

import requests_mock

from woo_publications.utils.tests.vcr import VCRMixin

from ..models import InformationCategory


class TestUpdateInformationCategoriesFromWaardenlijstCommand(VCRMixin, TestCase):
    def test_happy_flow(self):
        assert not InformationCategory.objects.exists()

        call_command("update_information_categories_from_waardenlijst")

        self.assertEqual(InformationCategory.objects.count(), 18)

    def test_command_with_file_path_flag(self):
        assert not InformationCategory.objects.exists()

        with tempfile.NamedTemporaryFile(suffix=".json") as file:
            file_path = file.name
            assert isinstance(file_path, str)

            call_command(
                "update_information_categories_from_waardenlijst", file_path=file_path
            )

        self.assertEqual(InformationCategory.objects.count(), 18)

    @requests_mock.Mocker()
    def test_raise_command_error(self, m):
        m.register_uri(requests_mock.ANY, requests_mock.ANY, status_code=400)
        assert not InformationCategory.objects.exists()

        with self.assertRaisesMessage(
            CommandError,
            "Got an unexpected response status code when retrieving the value list data: 400.",
        ):
            call_command("update_information_categories_from_waardenlijst")
