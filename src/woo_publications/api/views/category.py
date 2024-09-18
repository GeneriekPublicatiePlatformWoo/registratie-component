from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from woo_publications.metadata.models import InformatieCategorie

from ..filterset.category import InformatieCategorieFilterset
from ..serializer.category import InformatieCategorieSerializer


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
class InformatieCategorieViewset(
    ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = InformatieCategorie.objects.all()
    serializer_class = InformatieCategorieSerializer
    filterset_class = InformatieCategorieFilterset
