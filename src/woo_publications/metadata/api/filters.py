from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from woo_publications.api.filters import URLFilter

from ..constants import OrganisationActive, Origins
from ..models import InformationCategory, Organisation


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


class OrganisationFilterSet(FilterSet):
    identifier = URLFilter(
        lookup_expr="exact",
        help_text=_(
            "Search the organisation based on the unique IRI that identifies a specific organisation."
        ),
    )
    naam = filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Search the organisation based on the name of the organisation."),
    )
    oorsprong = filters.ChoiceFilter(
        help_text=_("Search the organisation based on the origin of the organisation."),
        choices=Origins.choices,
    )
    is_actief = filters.ChoiceFilter(
        help_text=_("Filter the organisations depending if they are active or not."),
        choices=OrganisationActive.choices,
        method="filter_is_actief",
    )

    class Meta:
        model = Organisation
        fields = (
            "identifier",
            "naam",
            "oorsprong",
            "is_actief",
        )

    def filter_is_actief(self, queryset, name, value):
        match (value):
            case OrganisationActive.inactive:
                return queryset.filter(is_actief=False)
            case OrganisationActive.active:
                return queryset.filter(is_actief=True)
            case OrganisationActive.all:
                return queryset

        return queryset.none()
