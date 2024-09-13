from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from woo_publications.api.models import InformatieCategorie


class InformatieCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformatieCategorie
        fields = (
            "url",
            "identifier",
            "name",
            "name_plural",
            "definition",
            "origin",
            "order",
        )
        extra_kwargs = {
            "url": {
                "view_name": "api:informatiecategorie-detail",
                "lookup_field": "pk",
                "help_text": _(
                    "De unieke URL van deze informatie categorie binnen deze API."
                ),
            },
        }
