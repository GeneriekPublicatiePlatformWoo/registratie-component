from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from ..models import InformationCategory, Organisation, Theme
from .filters import InformationCategoryFilterSet, OrganisationFilterSet
from .serializer import (
    InformationCategorySerializer,
    OrganisationSerializer,
    ThemeSerializer,
)


@extend_schema(tags=["Informatiecategorieën"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available information categories."),
        description=_(
            "Returns a paginated result list of existing information categories."
        ),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific information category."),
        description=_("Retrieve a specific information category."),
    ),
)
class InformationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterSet
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["Organisaties"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available organisations."),
        description=_("Returns a paginated result list of existing organisations."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific organisation."),
        description=_("Retrieve a specific organisation."),
    ),
    create=extend_schema(
        summary=_("Create a organisation."),
        description=_("Create a organisation."),
    ),
    partial_update=extend_schema(
        summary=_("Update a organisation partially."),
        description=_("Update a organisation partially."),
    ),
    update=extend_schema(
        summary=_("Update a organisation entirely."),
        description=_("Update a organisation entirely."),
    ),
)
class OrganisationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filterset_class = OrganisationFilterSet
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["Themas"])
@extend_schema_view(
    list=extend_schema(
        summary=_("All available themes."),
        description=_("Returns a paginated result list of existing themes."),
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a specific theme."),
        description=_("Retrieve a specific theme."),
    ),
)
class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all().order_by("path")
    serializer_class = ThemeSerializer
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        # for list operations, restrict to the root nodes and let the serializer
        # look up the children.
        # See #63 for the ticket to optimize this!
        if self.action == "list":
            qs = qs.filter(depth=1)
        return qs
