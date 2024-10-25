from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import Document, Publication


class DocumentSerializer(serializers.ModelSerializer):
    publicatie = serializers.SlugRelatedField(
        queryset=Publication.objects.all(),
        slug_field="uuid",
        help_text=_("The unique identifier of the publication."),
    )

    class Meta:  # type: ignore
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
        )


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Publication
        fields = (
            "uuid",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "registratiedatum",
        )
        extra_kwargs = {
            "uuid": {
                "read_only": True,
            },
            "registratiedatum": {
                "read_only": True,
            },
        }
