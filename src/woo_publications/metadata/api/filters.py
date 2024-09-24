from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from woo_publications.api.filters import URLFilter

from ..models import InformationCategory, Theme


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


class ThemeFilterSet(FilterSet):
    identifier = URLFilter(
        lookup_expr="exact",
        help_text=_(
            "Search the theme based on the unique IRI that identifies a specific theme."
        ),
    )
    naam = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Search the theme based on the name of the theme."),
    )
    super = filters.BooleanFilter(
        method="filter_super",
        help_text=_(
            "Displays either all or no super themes (filters if depth is 1 or higher)"
        ),
    )

    class Meta:
        model = Theme
        fields = ("identifier", "naam", "super")

    def filter_super(self, queryset, name, value):
        if value:
            return queryset.filter(depth=1)
        return queryset.filter(depth__gt=1)
