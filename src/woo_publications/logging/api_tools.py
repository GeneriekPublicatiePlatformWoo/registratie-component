from django.db.models import Model

from rest_framework import mixins

from .logevent import (
    audit_api_create,
    audit_api_delete,
    audit_api_read,
    audit_api_update,
)

__all__ = [
    "AuditTrailCreateMixin",
    "AuditTrailRetrieveMixin",
    "AuditTrailUpdateMixin",
    "AuditTrailDestroyMixin",
    "AuditTrailViewsetMixin",
]


class AuditTrailCreateMixin(mixins.CreateModelMixin):
    def _get_object(self, response):
        filter = {self.lookup_field: response.data[self.lookup_field]}  # type: ignore
        return self.get_queryset().get(**filter)  # type: ignore

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        obj: Model = self._get_object(response)

        audit_api_create(
            obj,
            request.headers["AUDIT_USER_ID"],
            request.headers["AUDIT_USER_REPRESENTATION"],
            response.status_code,
            response.data,
            request.headers["AUDIT_REMARKS"],
        )

        return response


class AuditTrailRetrieveMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        audit_api_read(
            self.get_object(),  # type: ignore
            request.headers["AUDIT_USER_ID"],
            request.headers["AUDIT_USER_REPRESENTATION"],
            response.status_code,
            request.headers["AUDIT_REMARKS"],
        )

        return response


class AuditTrailUpdateMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        audit_api_update(
            self.get_object(),  # type: ignore
            request.headers["AUDIT_USER_ID"],
            request.headers["AUDIT_USER_REPRESENTATION"],
            response.status_code,
            response.data,
            request.headers["AUDIT_REMARKS"],
        )

        return response


class AuditTrailDestroyMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        object: Model = self.get_object()  # type: ignore
        response = super().destroy(request, *args, **kwargs)

        audit_api_delete(
            object,
            request.headers["AUDIT_USER_ID"],
            request.headers["AUDIT_USER_REPRESENTATION"],
            response.status_code,
            request.headers["AUDIT_REMARKS"],
        )

        return response


class AuditTrailViewsetMixin(
    AuditTrailCreateMixin,
    AuditTrailRetrieveMixin,
    AuditTrailUpdateMixin,
    AuditTrailDestroyMixin,
):
    pass
