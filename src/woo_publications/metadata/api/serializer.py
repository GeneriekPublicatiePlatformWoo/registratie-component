from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import InformationCategory, Theme


class InformationCategorySerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = InformationCategory
        fields = (
            "uuid",
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
            "uuid",
            "identifier",
            "naam",
            "depth",
        )
        extra_kwargs = {
            "depth": {
                "help_text": _(
                    "Indicates how deeply the theme is nested within its parents. "
                    "A value of one means it's a root node, a value of 2 is a child, "
                    "a value of three is a grandchild etc."
                )
            },
        }
