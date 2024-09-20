from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from woo_publications.metadata.models import InformationCategory

from ..filterset.category import InformationCategoryFilterset
from ..serializer.category import InformationCategorySerializer


@extend_schema(tags=["informatie categorie"])
@extend_schema_view(
    list=extend_schema(
        summary=_("Alle informatie categorieën opvragen."),
        description=_("Alle informatie categorieën opvragen."),
    ),
    retrieve=extend_schema(
        summary="Een specifiek informatie categorie opvragen.",
        description="Een specifiek informatie categorie opvragen.",
    ),
)
class InformationCategoryViewset(
    ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filterset_class = InformationCategoryFilterset
