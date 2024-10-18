from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias, overload

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


JSONPrimitive: TypeAlias = str | int | float | bool | None

JSONValue: TypeAlias = "JSONPrimitive | JSONObject | list[JSONValue]"

JSONObject: TypeAlias = dict[str, JSONValue]


@overload
def _audit_event(
    content_object: models.Model,
    event: Events,
    user_id: str,
    user_display: str,
    django_user: None,
    **kwargs,
) -> None:
    pass


@overload
def _audit_event(
    content_object: models.Model,
    event: Events,
    user_id: None,
    user_display: None,
    django_user: User,
    **kwargs,
) -> None:
    pass


def _audit_event(
    content_object: models.Model,
    event: Events,
    user_id=None,
    user_display=None,
    django_user=None,
    **kwargs,
) -> None:

    from .models import TimelineLogProxy

    assert django_user or user_id and user_display

    identifier = "Unknown"
    display_name = "Unknown"

    if django_user:
        identifier = django_user.id
        display_name = django_user.get_full_name() or "unknown"

    if user_id and user_display:
        identifier = user_id
        display_name = user_display

    extra_data = {
        "event": event,
        "acting_user": {
            "identifier": identifier,
            "display_name": display_name,
        },
        **kwargs,
    }

    TimelineLogProxy.objects.create(
        content_object=content_object,
        extra_data=extra_data,
        user=django_user,
    )


# Admin tooling:


def audit_admin_create(
    content_object: models.Model,
    django_user: User,
    object_data: JSONObject,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.create,
        user_id=None,
        user_display=None,
        django_user=django_user,
        object_data=object_data,
    )


def audit_admin_read(
    content_object: models.Model,
    django_user: User,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.read,
        user_id=None,
        user_display=None,
        django_user=django_user,
    )


def audit_admin_update(
    content_object: models.Model,
    django_user: User,
    object_data: dict[str, any],  # type: ignore
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.update,
        user_id=None,
        user_display=None,
        django_user=django_user,
        object_data=object_data,
    )


def audit_admin_delete(
    content_object: models.Model,
    django_user: User,
) -> None:
    _audit_event(
        content_object=content_object,
        event=Events.delete,
        user_id=None,
        user_display=None,
        django_user=django_user,
    )


# Api tooling:


def audit_api_create(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    object_data: JSONObject,
    remarks: str,
) -> None:
    _audit_event(
        content_object,
        Events.create,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
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
) -> None:
    _audit_event(
        content_object,
        Events.read,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        status_code=status_code,
        remarks=remarks,
    )


def audit_api_update(
    content_object: models.Model,
    user_id: str,
    user_display: str,
    status_code: int,
    object_data: JSONObject,
    remarks: str,
) -> None:
    _audit_event(
        content_object,
        Events.update,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
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
) -> None:
    _audit_event(
        content_object,
        Events.delete,
        user_id=user_id,
        user_display=user_display,
        django_user=None,
        status_code=status_code,
        remarks=remarks,
    )
