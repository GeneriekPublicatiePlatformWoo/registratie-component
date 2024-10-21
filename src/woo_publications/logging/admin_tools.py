from django.db import models
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


class AdminAuditLogMixin:
    """
    Enable audit logging in the admin.

    Add, change, delete and view action will be logged.
    """

    model: type[models.Model]

    def log_addition(self, request, object, message):
        assert isinstance(request.user, User)
        audit_admin_create(
            content_object=object,
            django_user=request.user,
            object_data=serialize_instance(object),
        )

        return super().log_addition(request, object, message)  # type: ignore reportAttributeAccessIssue

    def log_change(self, request, object, message):
        assert isinstance(request.user, User)
        audit_admin_update(
            content_object=object,
            django_user=request.user,
            object_data=serialize_instance(object),
        )

        return super().log_change(request, object, message)  # type: ignore reportAttributeAccessIssue

    def log_deletion(self, request, object, object_repr):
        assert isinstance(request.user, User)
        audit_admin_delete(
            content_object=object,
            django_user=request.user,
            object_data=serialize_instance(object),
        )

        return super().log_deletion(request, object, object_repr)  # type: ignore reportAttributeAccessIssue

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if object_id and request.method == "GET":
            object = self.model.objects.get(pk=object_id)

            assert isinstance(request.user, User)
            audit_admin_read(content_object=object, django_user=request.user)

        return super().change_view(request, object_id, form_url, extra_context)  # type: ignore reportAttributeAccessIssue

    def get_formset_kwargs(self, request, obj, inline, prefix):
        kwargs = super().get_formset_kwargs(request, obj, inline, prefix)  # type: ignore reportAttributeAccessIssue
        kwargs["_django_user"] = request.user
        return kwargs


class AuditLogInlineformset(BaseInlineFormSet):
    """
    Custom formset class for admin inlines to enable audit logging.

    Add and update actions on related objects are logged.
    """

    def __init__(self, *args, **kwargs):
        self.django_user = kwargs.pop("_django_user", None)
        super().__init__(*args, **kwargs)

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit)

        audit_admin_create(
            content_object=obj,
            django_user=self.django_user,
            object_data=serialize_instance(obj),
        )

        return obj

    def save_existing(self, form, obj, commit=True):
        audit_admin_update(
            content_object=obj,
            django_user=self.django_user,
            object_data=serialize_instance(obj),
        )

        return super().save_existing(form, obj, commit)
