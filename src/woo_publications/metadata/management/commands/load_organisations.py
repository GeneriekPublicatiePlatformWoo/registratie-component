from django.core.management.commands import loaddata

from ...keep_organisations_active import keep_organisations_active


class Command(loaddata.Command):
    help = "Load organisations from fixture file"

    def handle(self, *args, **options):
        with keep_organisations_active():
            super().handle(*args, **options)
