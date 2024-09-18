from glom import glom, PathAccessError, Path, T
import json
import requests

from django.core.management.base import BaseCommand, CommandError

from woo_publications.metadata.constants import InformatieCategorieOrigins


class Command(BaseCommand):
    help = "Used to fetch the gov waardenlijsten data and turn them into a fixture to load the data into the db."

    def handle(self, *args, **options):
        r = requests.get("https://repository.officiele-overheidspublicaties.nl/waardelijsten/scw_woo_informatiecategorieen/3/json/scw_woo_informatiecategorieen_3.json")
        if r.status_code != 200:
            raise CommandError("Could not connect with url.")

        data = r.json()
        if not data:
            raise CommandError("Could not retrieve json from url.")

        fixture = []

        for waardenlijst in data:
            # filter out all ids that aren't waardenlijsten
            if not waardenlijst.get("@id").split("/")[-1].startswith("c_"):
                continue

            fixture_entry = {
                "pk": None,
                "model": "metadata.informatiecategorie"
            }

            fields = {
                "identifier": waardenlijst.get("@id"),
                "naam": glom(waardenlijst, Path("http://www.w3.org/2004/02/skos/core#prefLabel", T[0]["@value"]), skip_exc=PathAccessError),
                "naam_meervoud": glom(waardenlijst, Path("https://identifier.overheid.nl/tooi/def/ont/prefLabelVoorGroepen", T[0]["@value"]), skip_exc=PathAccessError),
                "definitie": glom(waardenlijst, Path("http://www.w3.org/2004/02/skos/core#definition", T[0]["@value"]), skip_exc=PathAccessError),
                "oorsprong": InformatieCategorieOrigins.value_list,
                "order": int(glom(waardenlijst, Path("http://www.w3.org/ns/shacl#order", T[0]["@value"]), skip_exc=PathAccessError))
            }

            fixture_entry["fields"] = fields
            fixture.append(fixture_entry)

        with open('src/woo_publications/fixtures/waardenlijst.json', 'w', encoding='utf-8') as f:
            json.dump(fixture, f, ensure_ascii=False, indent=4)

