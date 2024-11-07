from typing import override

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets

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
    create=extend_schema(
        summary=_("Register a document's metadata."),
        description=_(
            "Creating a document results in the registration of the metadata and "
            "prepares the client for the upload of the binary data.\n\n"
            "The document (metadata) is immediately registered in the underlying "
            "Documents API, and you receive an array of `bestandsdelen` in the "
            "response data to upload the actual binary data of the document.\n\n"
            "Note that the record in the underlying Documents API remains locked until "
            "all file parts have been provided.\n\n"
            "**NOTE**\n"
            "This requires the global configuration to be set up via the admin "
            "interface. You must:\n\n"
            "* configure and select the Documents API to use\n"
            "* specify the organisation RSIN for the created documents"
        ),
    ),
)
class DocumentViewSet(
    AuditTrailViewSetMixin,
    mixins.CreateModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = Document.objects.order_by("-creatiedatum")
    serializer_class = DocumentSerializer
    filterset_class = DocumentFilterSet
    lookup_field = "uuid"
    lookup_value_converter = "uuid"

    @override
    @transaction.atomic()
    def perform_create(self, serializer):
        """
        Register the metadata in the database and create the record in the Documents API.
        """
        super().perform_create(serializer)
        assert serializer.instance is not None
        woo_document = serializer.instance
        assert isinstance(woo_document, Document)
        woo_document.register_in_documents_api(
            build_absolute_uri=self.request.build_absolute_uri,
        )


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
    lookup_value_converter = "uuid"
