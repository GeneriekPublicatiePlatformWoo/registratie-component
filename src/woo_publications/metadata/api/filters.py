from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from woo_publications.api.filters import URLFilter

from ..models import InformationCategory


class InformationCategoryFilterSet(FilterSet):
    identifier = URLFilter(
        lookup_expr="exact",
        help_text=_(
            "Search the information category based on the unique IRI that identifies a specific category."
        ),
    )
    naam = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_(
            "Search the information category based on the name of the category."
        ),
    )

    class Meta:
        model = InformationCategory
        fields = (
            "identifier",
            "naam",
        )
