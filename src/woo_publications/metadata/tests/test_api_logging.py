from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy

from .factories import InformationCategoryFactory, ThemeFactory

AUDIT_HEADERS = {
    "AUDIT_USER_REPRESENTATION": "username",
    "AUDIT_USER_ID": "id",
    "AUDIT_REMARKS": "remark",
}


class InformationCategoryLoggingTests(APITestCase):

    def test_retrieve_logging(self):
        information_category = InformationCategoryFactory.create()
        detail_url = reverse(
            "api:informationcategory-detail",
            kwargs={"uuid": str(information_category.uuid)},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        assert response.status_code == status.HTTP_200_OK
        log_records = TimelineLogProxy.objects.filter(
            content_type=ContentType.objects.get_for_model(information_category),
            object_id=information_category.pk,
            extra_data__event=Events.read,
        )
        self.assertEqual(log_records.count(), 1)


class ThemeLoggingTests(APITestCase):

    def test_retrieve_logging(self):
        theme = ThemeFactory.create()
        detail_url = reverse(
            "api:theme-detail",
            kwargs={"uuid": str(theme.uuid)},
        )

        response = self.client.get(detail_url, headers=AUDIT_HEADERS)

        assert response.status_code == status.HTTP_200_OK
        log_records = TimelineLogProxy.objects.filter(
            content_type=ContentType.objects.get_for_model(theme),
            object_id=theme.pk,
            extra_data__event=Events.read,
        )
        self.assertEqual(log_records.count(), 1)
