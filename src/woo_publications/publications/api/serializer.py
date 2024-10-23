from rest_framework import serializers

from ..models import Document, Publication


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Document
        fields = (
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
