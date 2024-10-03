import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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
