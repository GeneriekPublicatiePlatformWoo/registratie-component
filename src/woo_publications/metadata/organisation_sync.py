from pathlib import Path

from django.core import serializers

import requests
from glom import PathAccessError, T, glom

from woo_publications.metadata.constants import OrganisationOrigins
from woo_publications.metadata.models import Organisation

MUNICIPALITY_WAARDENLIJST_URL = (
    "https://repository.officiele-overheidspublicaties.nl/waardelijsten/"
    "rwc_gemeenten_compleet/4/json/"
    "rwc_gemeenten_compleet_4.json"
)
SO_WAARDENLIJST_URL = (
    "https://repository.officiele-overheidspublicaties.nl/waardelijsten/"
    "rwc_samenwerkingsorganisaties_compleet/1/json/"
    "rwc_samenwerkingsorganisaties_compleet_1.json"
)
OORG_WAARDENLIJST_URL = (
    "https://repository.officiele-overheidspublicaties.nl/waardelijsten/"
    "rwc_overige_overheidsorganisaties_compleet/8/json/"
    "rwc_overige_overheidsorganisaties_compleet_8.json"
)

MUNICIPALITY_WAARDENLIJST_TYPE = "https://identifier.overheid.nl/tooi/def/ont/Gemeente"
SO_WAARDENLIJST_TYPE = (
    "https://identifier.overheid.nl/tooi/def/ont/Samenwerkingsorganisatie"
)
OORG_WAARDENLIJST_TYPE = (
    "https://identifier.overheid.nl/tooi/def/ont/Overheidsorganisatie"
)
WAARDENLIJST_URLS = [
    MUNICIPALITY_WAARDENLIJST_URL,
    SO_WAARDENLIJST_URL,
    OORG_WAARDENLIJST_URL,
]

TYPE_MAPPING = [
    (
        MUNICIPALITY_WAARDENLIJST_URL,
        MUNICIPALITY_WAARDENLIJST_TYPE,
        OrganisationOrigins.municipality_list,
    ),
    (SO_WAARDENLIJST_URL, SO_WAARDENLIJST_TYPE, OrganisationOrigins.so_list),
    (OORG_WAARDENLIJST_URL, OORG_WAARDENLIJST_TYPE, OrganisationOrigins.oorg_list),
]

SPEC = {
    "identifier": "@id",
    "naam": T["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"],
}


class OrganisatieWaardenlijstError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def update_organisation(file_path: Path):
    for waardenlijst_url, waardenlijst_type, oorsprong in TYPE_MAPPING:
        try:
            response = requests.get(waardenlijst_url)
        except requests.RequestException as err:
            raise OrganisatieWaardenlijstError(
                f"Could not retrieve the value list data from url `{waardenlijst_url}`."
            ) from err

        try:
            response.raise_for_status()
        except requests.RequestException as err:
            raise OrganisatieWaardenlijstError(
                "Got an unexpected response status code when retrieving the value "
                f"list data from url `{waardenlijst_url}`: {response.status_code}."
            ) from err

        data = response.json()
        if not data:
            raise OrganisatieWaardenlijstError(
                f"Received empty data from value list `{waardenlijst_url}`."
            )

        for waardenlijst in data:
            # filter out all ids that aren't waardenlijsten
            if not waardenlijst["@type"][0] == waardenlijst_type:
                continue

            fields = glom(waardenlijst, SPEC, skip_exc=PathAccessError)
            Organisation.objects.update_or_create(
                identifier=waardenlijst["@id"],
                defaults={**fields, "oorsprong": oorsprong},
            )

    value_list_organisations = Organisation.objects.exclude(
        oorsprong=OrganisationOrigins.custom_entry
    )

    fixture_data = serializers.serialize(
        "json",
        value_list_organisations,
        indent=4,
        use_natural_primary_keys=True,
        fields=(
            "uuid",
            "identifier",
            "naam",
            "oorsprong",
        ),
    )

    with open(file_path, "w") as outfile:
        outfile.write(fixture_data)
