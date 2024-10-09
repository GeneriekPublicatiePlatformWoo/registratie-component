from io import StringIO
from pathlib import Path

from django.core.management import call_command

import requests
from glom import PathAccessError, T, glom

from .constants import InformationCategoryOrigins
from .models import InformationCategory

WAARDENLIJST_URL = (
    "https://repository.officiele-overheidspublicaties.nl/waardelijsten/scw_woo_informatiecategorieen/3/json/scw_woo_informatiecategorieen_3.json"
)

SPEC = {
    "naam": T["http://www.w3.org/2004/02/skos/core#prefLabel"][0]["@value"],
    "naam_meervoud": T[
        "https://identifier.overheid.nl/tooi/def/ont/prefLabelVoorGroepen"
    ][0]["@value"],
    "definitie": T["http://www.w3.org/2004/02/skos/core#definition"][0]["@value"],
    "order": T["http://www.w3.org/ns/shacl#order"][0]["@value"],
}


class InformatieCategoryWaardenlijstError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def update_informatie_category(file_path: Path):
    try:
        response = requests.get(WAARDENLIJST_URL)
    except requests.RequestException as err:
        raise InformatieCategoryWaardenlijstError(
            "Could not retrieve the value list data."
        ) from err

    try:
        response.raise_for_status()
    except requests.RequestException as err:
        raise InformatieCategoryWaardenlijstError(
            f"Got an unexpected response status code when retrieving the value list data: {response.status_code}."
        ) from err

    data = response.json()
    if not data:
        raise InformatieCategoryWaardenlijstError(
            "Received empty data from value list."
        )

    for waardenlijst in data:
        # filter out all ids that aren't waardenlijsten
        if (
            not waardenlijst.get("@type")[0]
            == "http://www.w3.org/2004/02/skos/core#Concept"
        ):
            continue

        fields = glom(waardenlijst, SPEC, skip_exc=PathAccessError)

        if fields:
            fields["oorsprong"] = InformationCategoryOrigins.value_list
            InformationCategory.objects.update_or_create(
                identifier=waardenlijst["@id"], defaults=fields
            )

    to_export = InformationCategory.objects.filter(
        oorsprong=InformationCategoryOrigins.value_list
    ).values_list("pk", flat=True)

    call_command(
        "dumpdata",
        "metadata.informationcategory",
        format="json",
        indent=4,
        natural_primary=True,
        pks=",".join([str(pk) for pk in to_export]),
        output=file_path,
        stdout=StringIO(),
    )
