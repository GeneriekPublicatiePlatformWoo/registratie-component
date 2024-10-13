from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import Publication
from .filters import PublicationFilterSet
from .serializer import PublicationSerializer


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
class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.order_by("-registratiedatum")
    serializer_class = PublicationSerializer
    filterset_class = PublicationFilterSet
    lookup_field = "uuid"
