from rest_framework import serializers

from ..models import Publication


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
