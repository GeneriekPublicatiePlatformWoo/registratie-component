from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from ..models import Document, Publication


class DocumentFilterSet(FilterSet):
    publication = filters.UUIDFilter(
        field_name="publication__uuid",
        lookup_expr="exact",
        help_text=_(
            "Search the document based on the unique identifier that represents a publication.."
        ),
    )
    sorteer = filters.OrderingFilter(
        help_text=_("Order on."),
        fields=(
            "creatiedatum",
            "officiele_titel",
            "verkorte_titel",
        ),
    )

    class Meta:
        model = Document
        fields = (
            "publication",
            "sorteer",
        )


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
        fields = ("sorteer",)
