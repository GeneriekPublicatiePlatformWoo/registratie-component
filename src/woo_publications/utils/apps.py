from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "woo_publications.utils"

    def ready(self):
        from . import checks  # noqa
