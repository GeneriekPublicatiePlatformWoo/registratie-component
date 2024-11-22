from typing import TypedDict

from django.conf import settings as django_settings
from django.http import HttpRequest


class SettingsContext(TypedDict):
    settings: dict[str, str]


def settings(request: HttpRequest) -> SettingsContext:
    public_settings = (
        "PROJECT_NAME",
        "RELEASE",
        "GIT_SHA",
    )
    context: SettingsContext = {
        "settings": {k: getattr(django_settings, k) for k in public_settings},
    }
    return context
