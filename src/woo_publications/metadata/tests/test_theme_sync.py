import tempfile
from io import StringIO
from pathlib import Path
from uuid import uuid4

from django.core.management import call_command
from django.test import TestCase

import requests
import requests_mock

from woo_publications.utils.tests.vcr import VCRMixin

from ..models import Theme
from ..theme_sync import ThemeWaardenlijstError, update_theme


class UpdateThemeTestCase(VCRMixin, TestCase):
    def test_data_gets_stored_and_turned_into_fixture(self):
        assert not Theme.objects.exists()

        with tempfile.NamedTemporaryFile(suffix=".json") as file:
            file_path = Path(file.name)

            update_theme(file_path)

            with self.subTest("database populated"):
                self.assertEqual(Theme.objects.count(), 92)

            with self.subTest("user content does not cause conflicts"):
                theme = Theme.objects.order_by("pk").last()
                assert theme is not None

                theme.identifier = "https://something.else"
                theme.uuid = uuid4()
                theme.path = theme.path + "1"
                theme.save()

                call_command("loaddata", file_path, stdout=StringIO())

                self.assertEqual(Theme.objects.count(), 93)

    @requests_mock.Mocker()
    def test_request_get_raises_valid_exception(self, m):
        m.register_uri(
            requests_mock.ANY, requests_mock.ANY, exc=requests.RequestException
        )
        assert not Theme.objects.exists()

        with tempfile.NamedTemporaryFile(suffix=".json") as file:
            file_path = Path(file.name)

            with self.assertRaisesMessage(
                ThemeWaardenlijstError,
                "Could not retrieve the value list data.",
            ):
                update_theme(file_path)

    @requests_mock.Mocker()
    def test_request_get_invalid_status_code(self, m):
        m.register_uri(requests_mock.ANY, requests_mock.ANY, status_code=400)
        assert not Theme.objects.exists()

        with tempfile.NamedTemporaryFile(suffix=".json") as file:
            file_path = Path(file.name)

            with self.assertRaisesMessage(
                ThemeWaardenlijstError,
                "Got an unexpected response status code when retrieving the value list data: 400.",
            ):
                update_theme(file_path)

    @requests_mock.Mocker()
    def test_request_has_no_data(self, m):
        m.register_uri(requests_mock.ANY, requests_mock.ANY, status_code=200, json=[])
        assert not Theme.objects.exists()

        with tempfile.NamedTemporaryFile(suffix=".json") as file:
            file_path = Path(file.name)

            with self.assertRaisesMessage(
                ThemeWaardenlijstError,
                "Received empty data from value list.",
            ):
                update_theme(file_path)
