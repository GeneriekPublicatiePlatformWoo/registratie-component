from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from woo_publications.metadata.models import InformatieCategorie

from .custom_filters import URLFilter


class InformatieCategorieFilterset(FilterSet):
    identifier = URLFilter(
        lookup_expr="exact",
        help_text=_(
            "Search the information category based on the unique URI that identifies a specific category."
        ),
    )
    naam = filters.CharFilter(
        lookup_expr="exact",
        help_text=_(
            "Search the information category based on the name of the category."
        ),
    )

    class Meta:
        model = InformatieCategorie
        fields = (
            "identifier",
            "naam",
        )
