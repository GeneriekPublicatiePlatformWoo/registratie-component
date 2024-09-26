from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

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
    sub_themes = serializers.ListField(
        child=RecursiveField(),
        help_text=_("The nested themes attached to this current theme."),
    )

    class Meta:  # type: ignore
        model = Theme
        fields = (
            "uuid",
            "identifier",
            "naam",
            "sub_themes",
        )
