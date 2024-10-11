from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db import models
    from ..accounts.models import User

from .constants import Events


def audit_event(
    content_object: models.Model,
    event: Events,
    user_id: str | None = None,
    user_display: str | None = None,
    django_user: User | None = None,
    **kwargs: dict[str, any]
) -> None:
    """ must contain either a django_user or user_id + user_display """

    from .models import TimelineLogProxy

    assert django_user or user_id and user_display

    extra_data = {
        "event": event,
        "acting_user": {
            "identifier": user_id or django_user.email,
            "display_name": user_display or django_user.get_full_name(),
        },
        **kwargs,
    }

    return TimelineLogProxy.objects.create(
        content_object=content_object,
        extra_data=extra_data,
        user=django_user,
    )


