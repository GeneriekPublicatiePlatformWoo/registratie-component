import json

from django.contrib.admin import ModelAdmin
from django.core.serializers import serialize
from django.forms import BaseInlineFormSet

from .logevent import (
    audit_admin_create,
    audit_admin_delete,
    audit_admin_read,
    audit_admin_update,
)

__all__ = ["AdminAuditLogMixin", "AuditLogInlineformset"]


def _serialize_field_data(obj):
    serialized_obj = serialize("json", [obj])
    return json.loads(serialized_obj)[0]["fields"]


class AdminAuditLogMixin(ModelAdmin):
    def log_addition(self, request, obj, message):  # type: ignore
        audit_admin_create(obj, request.user, _serialize_field_data(obj))

        return super().log_addition(request, obj, message)

    def log_change(self, request, obj, message):  # type: ignore
        audit_admin_update(obj, request.user, _serialize_field_data(obj))  # type: ignore

        return super().log_change(request, obj, message)

    def log_deletion(self, request, obj, object_repr):  # type: ignore
        audit_admin_delete(obj, request.user)  # type: ignore

        return super().log_deletion(request, obj, object_repr)

    def change_view(self, request, object_id, form_url="", extra_context=None):  # type: ignore
        if object_id and request.method == "GET":
            obj = self.model.objects.get(pk=object_id)

            audit_admin_read(obj, request.user)  # type: ignore

        return super().change_view(request, object_id, form_url, extra_context)

    def get_formset_kwargs(self, request, obj, inline, prefix):
        kwargs = super().get_formset_kwargs(request, obj, inline, prefix)
        kwargs["_django_user"] = request.user
        return kwargs


class AuditLogInlineformset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.django_user = kwargs.pop("_django_user", None)
        super().__init__(*args, **kwargs)

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit)

        audit_admin_create(obj, self.django_user, _serialize_field_data(obj))  # type: ignore

        return obj

    def save_existing(self, form, instance, commit=True):  # type: ignore
        audit_admin_create(instance, self.django_user, _serialize_field_data(instance))  # type: ignore

        return super().save_existing(form, instance, commit)
