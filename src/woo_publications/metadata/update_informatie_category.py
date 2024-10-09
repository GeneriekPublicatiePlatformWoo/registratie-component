from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command

import requests
from glom import PathAccessError, T, glom

from woo_publications.metadata.constants import InformationCategoryOrigins
from woo_publications.metadata.models import InformationCategory

SPEC = {
    "naam": T["http://www.w3.org/2004/02/skos/core#prefLabel"][0]["@value"],
    "naam_meervoud": T[
        "https://identifier.overheid.nl/tooi/def/ont/prefLabelVoorGroepen"
    ][0]["@value"],
    "definitie": T["http://www.w3.org/2004/02/skos/core#definition"][0]["@value"],
    "order": T["http://www.w3.org/ns/shacl#order"][0]["@value"],
}


class InformatieCategoryWaardenlijstError(Exception):
    pass


def update_informatie_category(file_path: str):
    if not file_path:
        file_path = str(
            Path(
                settings.BASE_DIR
                / "src"
                / "woo_publications"
                / "fixtures"
                / "informatie_category.json"
            )
        )

    response = requests.get(
        "https://repository.officiele-overheidspublicaties.nl/waardelijsten/scw_woo_informatiecategorieen/3/json/scw_woo_informatiecategorieen_3.json"
    )

    try:
        response.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        raise InformatieCategoryWaardenlijstError(
            "Could not connect with url."
        ) from err

    data = response.json()
    if not data:
        raise InformatieCategoryWaardenlijstError("Could not retrieve json from url.")

    for waardenlijst in data:
        # filter out all ids that aren't waardenlijsten
        if (
            not waardenlijst.get("@type")[0]
            == "http://www.w3.org/2004/02/skos/core#Concept"
        ):
            continue

        fields = glom(waardenlijst, SPEC, skip_exc=PathAccessError)
        fields["oorsprong"] = InformationCategoryOrigins.value_list

        if fields:
            InformationCategory.objects.update_or_create(
                identifier=waardenlijst.get("@id"), defaults=fields
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
