from __future__ import annotations

from django.db import models

from woo_publications.accounts.models import User
from woo_publications.typing import JSONObject

from .constants import Events
from .models import TimelineLogProxy
from .typing import MetadataDict

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


def _audit_event(
    *,
    content_object: models.Model,
    event: Events,
    user_id: str = "",
    user_display: str = "",
    django_user: User | None = None,
    **kwargs,
) -> None:
    if django_user is None and not (user_id and user_display):
        raise ValueError(
            "Provide either a Django user, or non-empty 'user_id' and 'user_display' "
            "parameters."
        )

    identifier: str | int
    display_name: str

    match django_user:
        case None:
            identifier = user_id
            display_name = user_display

        case User():
            identifier = user_id or django_user.pk
            display_name = (
                user_display or django_user.get_full_name() or django_user.username
            )

    metadata: MetadataDict = {
        "event": event,
        "acting_user": {
            "identifier": identifier,
            "display_name": display_name,
        },
    }

    TimelineLogProxy.objects.create(
        content_object=content_object,
        extra_data={
            **metadata,
            **kwargs,
        },
        user=django_user,
    )


# Admin tooling:


def audit_admin_create(
    *,
    content_object: models.Model,
    django_user: User,
    object_data: JSONObject,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.create,
        django_user=django_user,
        object_data=object_data,
    )


def audit_admin_read(
    *,
    content_object: models.Model,
    django_user: User,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.read,
        django_user=django_user,
    )


def audit_admin_update(
    *,
    content_object: models.Model,
    django_user: User,
    object_data: JSONObject,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.update,
        django_user=django_user,
        object_data=object_data,
    )


def audit_admin_delete(
    *,
    content_object: models.Model,
    django_user: User,
    object_data: JSONObject,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.delete,
        django_user=django_user,
        object_data=object_data,
    )


# Api tooling:


def audit_api_create(
    *,
    content_object: models.Model,
    user_id: str,
    user_display: str,
    object_data: JSONObject,
    remarks: str,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.create,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        object_data=object_data,
        remarks=remarks,
    )


def audit_api_read(
    *,
    content_object: models.Model,
    user_id: str,
    user_display: str,
    remarks: str,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.read,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        remarks=remarks,
    )


def audit_api_update(
    *,
    content_object: models.Model,
    user_id: str,
    user_display: str,
    object_data: JSONObject,
    remarks: str,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.update,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        object_data=object_data,
        remarks=remarks,
    )


def audit_api_delete(
    *,
    content_object: models.Model,
    user_id: str,
    user_display: str,
    object_data: JSONObject,
    remarks: str,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.delete,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        object_data=object_data,
        remarks=remarks,
    )
