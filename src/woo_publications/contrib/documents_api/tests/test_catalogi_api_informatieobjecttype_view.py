from uuid import uuid4

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class CatalogiAPIDocumentTypeViewTests(APITestCase):

    def test_dummy_data_returned(self):
        """
        Assert that we (initially) return dummy data.
        """
        uuid_str = str(uuid4())
        endpoint = reverse(
            "catalogi-informatieobjecttypen-detail", kwargs={"uuid": uuid_str}
        )

        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "url": f"http://testserver{endpoint}",
            "catalogus": "http://testserver/catalogi/api/v1/catalogussen/-fake-",
            "omschrijving": "Placeholder",
            "vertrouwelijkheidaanduiding": "openbaar",
            "beginGeldigheid": "2024-09-01",
            "concept": False,
            "informatieobjectcategorie": "Placeholder",
            "besluittypen": [],
            "zaaktypen": [],
        }
        self.assertEqual(response.json(), expected_data)
