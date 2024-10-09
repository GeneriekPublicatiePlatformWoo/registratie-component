from django.core.management.base import BaseCommand, CommandError

from woo_publications.metadata.update_informatie_category import (
    InformatieCategoryWaardenlijstError,
    update_informatie_category,
)


class Command(BaseCommand):
    help = "Used to fetch the gov waardenlijsten data and turn them into a fixture to load the data into the db."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file-path",
            action="store",
            help="The file path to where the fixture file will be created.",
            default=None,
        )

    def handle(self, *args, **options):
        try:
            update_informatie_category(options["file_path"])
        except InformatieCategoryWaardenlijstError as err:
            raise CommandError(err)
