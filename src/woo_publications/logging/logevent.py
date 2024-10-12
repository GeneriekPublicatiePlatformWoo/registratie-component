from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin

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
    **kwargs: dict[str, any],
) -> None:
    """must contain either a django_user or user_id + user_display"""

    from .models import TimelineLogProxy

    assert django_user or user_id and user_display

    extra_data = {
        "event": event,
        "acting_user": {
            "identifier": user_id or django_user.email,
            "display_name": user_display or django_user.get_display_name(),
        },
        **kwargs,
    }

    return TimelineLogProxy.objects.create(
        content_object=content_object,
        extra_data=extra_data,
        user=django_user,
    )


class AdminAuditLogMixin(ModelAdmin):
    def log_addition(self, request, obj, message):
        object_data = {
            field.name: str(getattr(obj, field.name))
            for field in obj._meta.fields
            if field.name not in ["id", "pk"]
        }
        audit_event(
            obj, Events.create, django_user=request.user, object_data=object_data
        )
        return super().log_addition(request, obj, message)

    def log_change(self, request, obj, message):
        new_data = {
            (field.name, str(getattr(obj, field.name))) for field in obj._meta.fields
        }
        changed_data = dict(new_data - self._old_model_data)
        audit_event(
            obj, Events.update, django_user=request.user, changed_data=changed_data
        )

        return super().log_change(request, obj, message)

    def log_deletion(self, request, obj, object_repr):
        audit_event(obj, Events.delete, django_user=request.user)
        return super().log_deletion(request, obj, object_repr)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if object_id:
            obj = self.model.objects.get(pk=object_id)
            # keep record of old data to compare in change log
            if request.method == "POST":
                self._old_model_data = {
                    (field.name, str(getattr(obj, field.name)))
                    for field in obj._meta.fields
                }

            audit_event(obj, Events.read, django_user=request.user)
        return super().change_view(request, object_id, form_url, extra_context)
