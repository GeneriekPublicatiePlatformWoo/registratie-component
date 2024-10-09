from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from woo_publications.metadata.update_informatie_category import (
    InformatieCategoryWaardenlijstError,
    update_informatie_category,
)


class Command(BaseCommand):
    help = "Retrieve the information categories from the value list published on overheid.nl and dump them as a fixture."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file-path",
            action="store",
            help="The file path to where the fixture file will be created.",
            default=Path(
                settings.BASE_DIR
                / "src"
                / "woo_publications"
                / "fixtures"
                / "informatie_category.json"
            ),
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        try:
            update_informatie_category(file_path)
        except InformatieCategoryWaardenlijstError as err:
            raise CommandError(err.message) from err
