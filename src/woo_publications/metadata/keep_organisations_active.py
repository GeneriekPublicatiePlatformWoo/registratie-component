from contextlib import contextmanager
from uuid import UUID

from django.db import transaction

from .models import Organisation


@contextmanager
@transaction.atomic
def keep_organisations_active():
    active_organisations_uuids: list[UUID] = list(
        Organisation.objects.filter(is_actief=True).values_list("uuid", flat=True)
    )
    try:
        yield
    finally:
        Organisation.objects.filter(uuid__in=active_organisations_uuids).update(
            is_actief=True
        )
