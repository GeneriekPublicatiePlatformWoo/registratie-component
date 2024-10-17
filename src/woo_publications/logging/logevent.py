from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db import models
    from ..accounts.models import User

from .constants import Events

__all__ = [
    # admin
    "audit_admin_create",
    "audit_admin_read",
    "audit_admin_update",
    "audit_admin_delete",
    # api
    "audit_api_create",
    "audit_api_read",
    "audit_api_update",
    "audit_api_delete",
]

"""must contain either a django_user or user_id + user_display"""


def _audit_event(
    content_object: models.Model,
    event: Events,
    user_id: str | None = None,
    user_display: str | None = None,
    django_user: User | None = None,
    **kwargs: any,
) -> None:

    from .models import TimelineLogProxy

    assert django_user or user_id and user_display

    extra_data = {
        "event": event,
        "acting_user": {
            "identifier": user_id or django_user.id,
            "display_name": user_display or django_user.get_full_name(),
        },
        **kwargs,
    }

    return TimelineLogProxy.objects.create(
        content_object=content_object,
        extra_data=extra_data,
        user=django_user,
    )


# Admin tooling:


def audit_admin_create(
    content_object: models.Model,
    django_user: User,
    object_data: dict[str, any],
):
    _audit_event(
        content_object, Events.create, django_user=django_user, object_data=object_data
    )


def audit_admin_read(
    content_object: models.Model,
    django_user: User,
):
    _audit_event(content_object, Events.read, django_user=django_user)


def audit_admin_update(
    content_object: models.Model,
    django_user: User,
    object_data: dict[str, any],
):
    _audit_event(
        content_object, Events.update, django_user=django_user, object_data=object_data
    )


def audit_admin_delete(
    content_object: models.Model,
    django_user: User,
):
    _audit_event(content_object, Events.delete, django_user=django_user)


# Api tooling:


def audit_api_create(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    object_data: dict[str, any],
    remarks: str,
):
    _audit_event(
        content_object,
        Events.create,
        user_id=user_id,
        user_display=user_display,
        status_code=status_code,
        object_data=object_data,
        remarks=remarks,
    )


def audit_api_read(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    remarks: str,
):
    _audit_event(
        content_object,
        Events.read,
        user_id=user_id,
        user_display=user_display,
        status_code=status_code,
        remarks=remarks,
    )


def audit_api_update(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    object_data: dict[str, any],
    remarks: str,
):
    _audit_event(
        content_object,
        Events.update,
        user_id=user_id,
        user_display=user_display,
        status_code=status_code,
        object_data=object_data,
        remarks=remarks,
    )


def audit_api_delete(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    remarks: str,
):
    _audit_event(
        content_object,
        Events.delete,
        user_id=user_id,
        user_display=user_display,
        status_code=status_code,
        remarks=remarks,
    )
