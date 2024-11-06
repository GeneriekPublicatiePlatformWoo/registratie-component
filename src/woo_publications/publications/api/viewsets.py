from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from woo_publications.logging.service import AuditTrailViewSetMixin

from ..models import Document, Publication
from .filters import DocumentFilterSet, PublicationFilterSet
from .serializers import DocumentSerializer, PublicationSerializer


@extend_schema(tags=["Documenten"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available documents."),
        description=_("Returns a paginated result list of existing documents."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific document."),
        description=_("Retrieve a specific document."),
    ),
)
class DocumentViewSet(AuditTrailViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.order_by("-creatiedatum")
    serializer_class = DocumentSerializer
    filterset_class = DocumentFilterSet
    lookup_field = "uuid"


@extend_schema(tags=["Publicaties"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available publications."),
        description=_("Returns a paginated result list of existing publications."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific publication."),
        description=_("Retrieve a specific publication."),
    ),
    create=extend_schema(
        summary=_("Create a publication."),
        description=_("Create a publication."),
    ),
    partial_update=extend_schema(
        summary=_("Update a publication partially."),
        description=_("Update a publication partially."),
    ),
    update=extend_schema(
        summary=_("Update a publication entirely."),
        description=_("Update a publication entirely."),
    ),
    destroy=extend_schema(
        summary=_("Destroy a publication."),
        description=_("Destroy a publication."),
    ),
)
class PublicationViewSet(AuditTrailViewSetMixin, viewsets.ModelViewSet):
    queryset = Publication.objects.order_by("-registratiedatum")
    serializer_class = PublicationSerializer
    filterset_class = PublicationFilterSet
    lookup_field = "uuid"
