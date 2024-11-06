from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from woo_publications.metadata.models import InformationCategory, Organisation

from ..models import Document, Publication


class DocumentSerializer(serializers.ModelSerializer):
    publicatie = serializers.SlugRelatedField(
        queryset=Publication.objects.all(),
        slug_field="uuid",
        help_text=_("The unique identifier of the publication."),
    )

    class Meta:  # pyright: ignore
        model = Document
        fields = (
            "uuid",
            "identifier",
            "publicatie",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "creatiedatum",
            "bestandsformaat",
            "bestandsnaam",
            "bestandsomvang",
            "registratiedatum",
            "laatst_gewijzigd_datum",
        )


class EigenaarSerializer(serializers.Serializer):
    weergave_naam = serializers.CharField(
        source="display_name",
        read_only=True,
        help_text=_("The display name of the user, as recorded in the audit trails."),
    )
    identifier = serializers.CharField(
        read_only=True,
        help_text=_(
            "The system identifier that uniquely identifies the user performing the action."
        ),
    )


class PublicationSerializer(serializers.ModelSerializer):
    eigenaar = EigenaarSerializer(
        source="get_owner",
        label=_("owner"),
        help_text=_("The creator of the publication, derived from the audit logs."),
        allow_null=True,
        read_only=True,
    )
    informatie_categorieen = serializers.SlugRelatedField(
        queryset=InformationCategory.objects.all(),
        slug_field="uuid",
        help_text=_(
            "The information categories clarify the kind of information present in the publication."
        ),
        many=True,
        allow_empty=False,
    )
    publisher = serializers.SlugRelatedField(
        queryset=Organisation.objects.filter(is_actief=True),
        slug_field="uuid",
        help_text=_("The organisation which publishes the publication."),
        many=False,
    )
    verantwoordelijke = serializers.SlugRelatedField(
        queryset=Organisation.objects.filter(is_actief=True),
        slug_field="uuid",
        help_text=_(
            "The organisation which is liable for the publication and it's contents."
        ),
        many=False,
        allow_null=True,
        required=False,
    )
    opsteller = serializers.SlugRelatedField(
        queryset=Organisation.objects.filter(is_actief=True),
        slug_field="uuid",
        help_text=_("The organisation which drafted the publication and it's content."),
        many=False,
        allow_null=True,
        required=False,
    )

    class Meta:  # pyright: ignore
        model = Publication
        fields = (
            "uuid",
            "informatie_categorieen",
            "publisher",
            "verantwoordelijke",
            "opsteller",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "eigenaar",
            "registratiedatum",
            "laatst_gewijzigd_datum",
        )
        extra_kwargs = {
            "uuid": {
                "read_only": True,
            },
            "registratiedatum": {
                "read_only": True,
            },
            "laatst_gewijzigd_datum": {
                "read_only": True,
            },
        }
