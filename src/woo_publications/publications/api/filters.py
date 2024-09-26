from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from ..models import Publication


class PublicationFilterSet(FilterSet):
    sorteer = filters.OrderingFilter(
        help_text=_("Order on."),
        fields=(
            "registratiedatum",
            "officiele_titel",
            "verkorte_titel",
        ),
    )

    class Meta:
        model = Publication
        fields = (
            "sorteer",
        )
