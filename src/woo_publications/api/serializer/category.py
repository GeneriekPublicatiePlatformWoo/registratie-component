from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from woo_publications.metadata.models import InformationCategory


class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationCategory
        fields = (
            "identifier",
            "naam",
            "naam_meervoud",
            "definitie",
            "oorsprong",
            "order",
        )
        extra_kwargs = {
            "order": {"help_text": _("The order number of the category.")},
        }
