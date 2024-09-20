from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions

from ..models import InformationCategory
from .filters import InformationCategoryFilterset
from .serializer import InformationCategorySerializer


@extend_schema(tags=["informatiecategorieën"])
@extend_schema_view(
    list=extend_schema(
        summary=_("Retrieve every information category."),
        description=_("Retrieve every information category."),
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific information category.",
        description="Retrieve a specific information category.",
    ),
)
class InformationCategoryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterset
    permission_classes = (permissions.AllowAny,)
