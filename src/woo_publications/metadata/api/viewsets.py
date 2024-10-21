from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from woo_publications.logging.service import AuditTrailRetrieveMixin

from ..models import InformationCategory, Theme
from .filters import InformationCategoryFilterSet
from .serializer import InformationCategorySerializer, ThemeSerializer


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
class InformationCategoryViewSet(
    AuditTrailRetrieveMixin, viewsets.ReadOnlyModelViewSet
):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterSet
    lookup_field = "uuid"


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
class ThemeViewSet(AuditTrailRetrieveMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all().order_by("path")
    serializer_class = ThemeSerializer
    lookup_field = "uuid"

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        # for list operations, restrict to the root nodes and let the serializer
        # look up the children.
        # See #63 for the ticket to optimize this!
        if self.action == "list":
            qs = qs.filter(depth=1)
        return qs
