from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import InformationCategory, Theme


class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
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
            "order": {
                "help_text": _(
                    "Controls the (default) ordering of categories in result lists."
                )
            },
        }


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Theme
        fields = (
            "identifier",
            "naam",
            "depth",
        )
        extra_kwargs = {
            "depth": {
                "help_text": _(
                    "Indicates the tree level of the theme."
                    "1 being a super theme and everything below it being a sub theme."
                )
            },
        }
