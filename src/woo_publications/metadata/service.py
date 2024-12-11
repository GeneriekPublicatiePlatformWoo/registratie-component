from django.conf import settings
from django.core.cache import cache

from .models import InformationCategory


def get_inspannings_verplichting():
    inspannings_verplicht = cache.get_or_set(
        "inspannings_verplichting",
        lambda: InformationCategory.objects.get(
            identifier=settings.INSPANNINGSVERPLICHTING_IDENTIFIER
        ),
        86400,
    )
    assert isinstance(inspannings_verplicht, InformationCategory)
    return inspannings_verplicht
