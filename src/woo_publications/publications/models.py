import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from zgw_consumers.constants import APITypes

# when the document isn't specified both the service and uuid needs to be unset
_DOCUMENT_NOT_SET = models.Q(document_service=None, document_uuid=None)
# when the document is specified both the service and uuid needs to be set
_DOCUMENT_SET = ~models.Q(document_service=None) & ~models.Q(document_uuid=None)


class Publication(models.Model):
    uuid = models.UUIDField(
        _("UUID"),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    officiele_titel = models.CharField(
        _("official title"),
        max_length=255,
    )
    verkorte_titel = models.CharField(
        _("short title"),
        max_length=255,
        blank=True,
    )
    omschrijving = models.TextField(_("description"), blank=True)
    registratiedatum = models.DateTimeField(
        _("created on"),
        auto_now_add=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the publication was registered in the "
            "database. Not to be confused with the creation date of the publication, "
            "which is usually *before* the registration date."
        ),
    )

    class Meta:  # type: ignore
        verbose_name = _("publication")
        verbose_name_plural = _("publications")

    def __str__(self):
        return self.officiele_titel


class Document(models.Model):
    publicatie = models.ForeignKey(
        Publication,
        verbose_name=_("publication"),
        help_text=_(
            "The publication that this document belongs to. A publication may have "
            "zero or more documents."
        ),
        on_delete=models.CASCADE,
    )
    document_service = models.ForeignKey(
        "zgw_consumers.Service",
        verbose_name=_("Documents API Service"),
        on_delete=models.PROTECT,
        limit_choices_to={
            "api_type": APITypes.drc,
        },
        null=True,
        blank=True,
    )
    document_uuid = models.UUIDField(
        _("document UUID"),
        help_text=_("The UUID of the API resource recorded in the Documenten API."),
        unique=False,
        editable=True,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        _("identifier"),
        help_text=_("The (primary) unique identifier."),
        max_length=255,
        unique=True,
    )
    officiele_titel = models.CharField(
        _("official title"),
        max_length=255,
    )
    verkorte_titel = models.CharField(
        _("short title"),
        max_length=255,
        blank=True,
    )
    omschrijving = models.TextField(_("description"), blank=True)
    creatiedatum = models.DateField(
        _("creation date"),
        help_text=_(
            "Date when the (physical) document came into existence. Not to be confused "
            "with the registration timestamp of the document - the creation date is "
            "typically *before* the registration date."
        ),
    )
    bestandsformaat = models.CharField(
        _("file format"),
        max_length=255,
        help_text=_(
            "TODO - placeholder accepting anything, in the future this will be "
            "validated against a reference value list."
        ),
        default="unknown",  # TODO: remove this once the formats are set up properly
    )
    bestandsnaam = models.CharField(
        _("file name"),
        max_length=255,
        help_text=_("File name 'on disk' of the document, e.g. 'gelakt-verslag.pdf'."),
        default="unknown.bin",  # TODO: remove this once we can enforce the blank=False
    )
    bestandsomvang = models.PositiveIntegerField(
        _("file size"),
        default=0,
        help_text=_("Size of the file on disk, in bytes."),
    )
    registratiedatum = models.DateTimeField(
        _("created on"),
        auto_now_add=True,
        editable=False,
        help_text=_(
            "System timestamp reflecting when the publication was registered in the "
            "database. Not to be confused with the creation date of the publication, "
            "which is usually *before* the registration date."
        ),
    )

    class Meta:  # type: ignore
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        constraints = [
            models.CheckConstraint(
                check=(_DOCUMENT_NOT_SET | _DOCUMENT_SET),
                name="documents_api_reference",
                violation_error_message=_(
                    "You must specify both the Documents API service and document UUID to identify a "
                    "document.",
                ),
            )
        ]

    def __str__(self):
        return self.officiele_titel
