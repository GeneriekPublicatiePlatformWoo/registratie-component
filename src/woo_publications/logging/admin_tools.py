from django.contrib.admin import ModelAdmin
from django.forms import BaseInlineFormSet

from woo_publications.accounts.models import User

from .logevent import (
    audit_admin_create,
    audit_admin_delete,
    audit_admin_read,
    audit_admin_update,
)
from .serializing import serialize_instance

__all__ = ["AdminAuditLogMixin", "AuditLogInlineformset"]


class AdminAuditLogMixin(ModelAdmin):
    def log_addition(self, request, object, message):
        assert isinstance(request.user, User)
        audit_admin_create(object, request.user, serialize_instance(object))

        return super().log_addition(request, object, message)

    def log_change(self, request, object, message):
        assert isinstance(request.user, User)
        audit_admin_update(object, request.user, serialize_instance(object))

        return super().log_change(request, object, message)

    def log_deletion(self, request, object, object_repr):
        assert isinstance(request.user, User)
        audit_admin_delete(object, request.user)

        return super().log_deletion(request, object, object_repr)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if object_id and request.method == "GET":
            object = self.model.objects.get(pk=object_id)

            assert isinstance(request.user, User)
            audit_admin_read(object, request.user)

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

        audit_admin_create(obj, self.django_user, serialize_instance(obj))

        return obj

    def save_existing(self, form, obj, commit=True):
        audit_admin_create(obj, self.django_user, serialize_instance(obj))

        return super().save_existing(form, obj, commit)
