from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from woo_publications.logging.constants import Events
from woo_publications.logging.models import TimelineLogProxy

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


class EigenaarSerializer(serializers.Serializer):
    display_name = serializers.CharField(
        read_only=True,
        help_text=_(
            "obtained from the audit trail request headers, extracted from the audit trails/log entries."
        ),
    )
    identifier = serializers.CharField(
        read_only=True,
        help_text=_(
            "arbitrary, unique-ish string. Could be a `sub` claim from OIDC, but for our perspective this data has no 'meaning'."
        ),
    )


class PublicationSerializer(serializers.ModelSerializer):
    eigenaar = serializers.SerializerMethodField(
        help_text=_("De eigenaar van de publicatie."), method_name="get_acting_user"
    )

    class Meta:  # type: ignore
        model = Publication
        fields = (
            "uuid",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "eigenaar",
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

    @extend_schema_field(EigenaarSerializer(many=False))
    def get_acting_user(self, obj):
        try:
            log = TimelineLogProxy.objects.for_object(obj).get(  # type: ignore reportAttributeAccessIssue
                extra_data__event=Events.create
            )
        except TimelineLogProxy.DoesNotExist:
            return {}

        return EigenaarSerializer(log.acting_user[0], context=self.context).data
