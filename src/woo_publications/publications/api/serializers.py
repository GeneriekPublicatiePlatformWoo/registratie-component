from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from woo_publications.api.constants import PublicationStatusOptions
from woo_publications.contrib.documents_api.client import FilePart
from woo_publications.metadata.models import InformationCategory, Organisation

from ..models import Document, Publication


class FilePartSerializer(serializers.Serializer[FilePart]):
    uuid = serializers.UUIDField(
        label=_("UUID"),
        help_text=_("The unique ID for a given file part for a document."),
    )
    url = serializers.URLField(
        label=_("url"),
        help_text=_("Endpoint where to submit the file part data to (**WIP**)."),
        default="https://example.com/dummy",
        read_only=True,
    )
    volgnummer = serializers.IntegerField(
        source="order",
        label=_("order"),
        help_text=_("Index of the filepart, indicating which chunk is being uploaded."),
    )
    omvang = serializers.IntegerField(
        source="size",
        label=_("size"),
        help_text=_(
            "Chunk size, in bytes. Large files must be cut up into chunks, where each "
            "chunk has an expected chunk size (configured on the Documents API "
            "server). A part is only considered complete once each chunk has binary "
            "data of exactly this size attached to it."
        ),
    )


class DocumentSerializer(serializers.ModelSerializer):
    publicatie = serializers.SlugRelatedField(
        queryset=Publication.objects.all(),
        slug_field="uuid",
        help_text=_("The unique identifier of the publication."),
    )
    bestandsdelen = FilePartSerializer(
        label=_("file parts"),
        help_text=_(
            "The expected file parts/chunks to upload the file contents. These are "
            "derived from the specified total file size (`bestandsomvang`) in the "
            "document create body."
        ),
        source="zgw_document.file_parts",
        many=True,
        read_only=True,
        allow_null=True,
    )

    class Meta:  # pyright: ignore
        model = Document
        fields = (
            "uuid",
            "identifier",
            "publicatie",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "publicatiestatus",
            "creatiedatum",
            "bestandsformaat",
            "bestandsnaam",
            "bestandsomvang",
            "registratiedatum",
            "laatst_gewijzigd_datum",
            "bestandsdelen",
        )


class EigenaarSerializer(serializers.Serializer):
    weergave_naam = serializers.CharField(
        source="display_name",
        read_only=True,
        help_text=_("The display name of the user, as recorded in the audit trails."),
    )
    identifier = serializers.CharField(
        read_only=True,
        help_text=_(
            "The system identifier that uniquely identifies the user performing the action."
        ),
    )


class PublicationSerializer(serializers.ModelSerializer):
    eigenaar = EigenaarSerializer(
        source="get_owner",
        label=_("owner"),
        help_text=_("The creator of the publication, derived from the audit logs."),
        allow_null=True,
        read_only=True,
    )
    informatie_categorieen = serializers.SlugRelatedField(
        queryset=InformationCategory.objects.all(),
        slug_field="uuid",
        help_text=_(
            "The information categories clarify the kind of information present in the publication."
        ),
        many=True,
        allow_empty=False,
    )
    publisher = serializers.SlugRelatedField(
        queryset=Organisation.objects.filter(is_actief=True),
        slug_field="uuid",
        help_text=_("The organisation which publishes the publication."),
        many=False,
    )
    verantwoordelijke = serializers.SlugRelatedField(
        queryset=Organisation.objects.filter(is_actief=True),
        slug_field="uuid",
        help_text=_(
            "The organisation which is liable for the publication and its contents."
        ),
        many=False,
        allow_null=True,
        required=False,
    )
    opsteller = serializers.SlugRelatedField(
        queryset=Organisation.objects.all(),
        slug_field="uuid",
        help_text=_("The organisation which drafted the publication and its content."),
        many=False,
        allow_null=True,
        required=False,
    )

    class Meta:  # pyright: ignore
        model = Publication
        fields = (
            "uuid",
            "informatie_categorieen",
            "publisher",
            "verantwoordelijke",
            "opsteller",
            "officiele_titel",
            "verkorte_titel",
            "omschrijving",
            "eigenaar",
            "publicatiestatus",
            "registratiedatum",
            "laatst_gewijzigd_datum",
        )
        extra_kwargs = {
            "uuid": {
                "read_only": True,
            },
            "registratiedatum": {
                "read_only": True,
            },
            "laatst_gewijzigd_datum": {
                "read_only": True,
            },
            "publicatiestatus": {
                "help_text": _(
                    "\n**Disclaimer**: you can't create a {} publication."
                ).format(PublicationStatusOptions.revoked.label.lower())
            },
        }

    def validate(self, attrs):
        self.instance: Publication

        if self.context["request"].method == "POST":
            if attrs.get("publicatiestatus") == PublicationStatusOptions.revoked:
                raise serializers.ValidationError(
                    {
                        "publicatiestatus": _(
                            "You cannot create a {} publication.".format(
                                PublicationStatusOptions.revoked.lower()
                            )
                        )
                    }
                )

        if (
            self.instance
            and self.instance.publicatiestatus == PublicationStatusOptions.revoked
        ):
            raise serializers.ValidationError(
                {
                    "publicatiestatus": _("You cannot modify a {} publication.").format(
                        PublicationStatusOptions.revoked.lower()
                    )
                }
            )

        return super().validate(attrs)
