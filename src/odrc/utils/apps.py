from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "odrc.utils"

    def ready(self):
        from . import checks  # noqa
