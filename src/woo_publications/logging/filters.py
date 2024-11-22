from django.contrib.contenttypes.models import ContentType
from django.db import models

from django_filters import filters
from django_filters.constants import EMPTY_VALUES

from .constants import Events
from .models import TimelineLogProxy

__all__ = [
    "OwnerFilter",
]


class OwnerFilter(filters.CharFilter):
    model: type[models.Model]

    def filter(self, qs, value: str):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()

        model = self.model
        publication_ct = ContentType.objects.get_for_model(model)

        object_pks = TimelineLogProxy.objects.filter(
            content_type=publication_ct,
            extra_data__event=Events.create,
            extra_data__acting_user__identifier=value,
        ).values_list("object_id", flat=True)

        return self.get_method(qs)(pk__in=[pk for pk in object_pks])
