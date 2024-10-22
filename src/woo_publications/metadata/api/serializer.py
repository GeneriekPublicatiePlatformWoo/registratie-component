from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ..constants import OrganisationOrigins
from ..models import InformationCategory, Organisation, Theme


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


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Organisation
        fields = ("uuid", "identifier", "naam", "oorsprong", "is_actief")
        read_only_fields = (
            "uuid",
            "idenitfier",
            "oorsprong",
        )
        extra_kwargs = {
            "naam": {
                "required": False,
                "help_text": _(
                    "The name of the organisation (can only be modified when `oorspring` is `{custom_entry}`).".format(
                        custom_entry=OrganisationOrigins.custom_entry
                    )
                ),
            },
            "is_actief": {
                "required": False,
            },
        }

    def update(self, instance, validated_data):
        if (
            validated_data.get("naam")
            and instance.oorsprong != OrganisationOrigins.custom_entry
        ):
            raise serializers.ValidationError(
                {
                    "naam": _(
                        "Only an organisation with the origin `{}` can update the `naam` field.".format(
                            OrganisationOrigins.custom_entry
                        )
                    )
                }
            )

        return super().update(instance, validated_data)


class ThemeSerializer(serializers.ModelSerializer):
    sub_themes = serializers.ListField(
        source="get_children",
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
