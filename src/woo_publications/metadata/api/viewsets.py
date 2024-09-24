from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from ..models import InformationCategory, Theme
from .filters import InformationCategoryFilterSet
from .serializer import InformationCategorySerializer, ThemeSerializer


@extend_schema(tags=["informatiecategorieën"])
@extend_schema_view(
    list=extend_schema(
        summary=_("all available information category."),
        description=_(
            "Returns a paginated result list of existing information categories."
        ),
    ),
    retrieve=extend_schema(
        summary="the specific information category.",
        description="Retrieve a specific information category.",
    ),
)
class InformationCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterSet
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=["themas"])
@extend_schema_view(
    list=extend_schema(
        summary=_("all available themes."),
        description=_("Returns a paginated result list of existing themes."),
    ),
    retrieve=extend_schema(
        summary="the specific theme.",
        description="Retrieve a specific theme.",
    ),
)
class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all().order_by("pk")
    serializer_class = ThemeSerializer
    lookup_field = "uuid"
    permission_classes = (permissions.AllowAny,)
