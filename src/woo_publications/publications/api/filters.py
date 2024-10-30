from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import FilterSet, filters

from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy

from ..models import Document, Publication


class DocumentFilterSet(FilterSet):
    # TODO: change this filter to custom named filter with `@extend_schema_field(UUID)` once bug is fixed in drf-spectacular
    publicatie = filters.ModelChoiceFilter(
        queryset=Publication.objects.all(),
        to_field_name="uuid",
        help_text=_(
            "Search the document based on the unique identifier (UUID) that represents a publication. "
            "**Disclaimer**: disregard the documented type `integer` the correct type is `UUID`."
        ),
    )
    identifier = filters.CharFilter(
        help_text="Search the document based on the identifier field.",
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
            "publicatie",
            "identifier",
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
    eigenaar = filters.CharFilter(
        help_text=_("Filter publications based on the owner identifier of the object."),
        method="filter_eigenaar",
    )

    class Meta:
        model = Publication
        fields = (
            "sorteer",
            "eigenaar",
        )

    def filter_eigenaar(self, queryset, name: str, value: str):
        publication_ct = ContentType.objects.get(
            app_label="publications",
            model="publication",
        )

        publication_object_ids = TimelineLogProxy.objects.filter(
            content_type=publication_ct,
            extra_data__event=Events.create,
            extra_data__acting_user__identifier=value,
        ).values_list("object_id", flat=True)

        return queryset.filter(pk__in=[id for id in publication_object_ids])
