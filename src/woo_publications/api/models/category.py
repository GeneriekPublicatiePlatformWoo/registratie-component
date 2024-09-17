from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel

from ..constants import InformatieCategorieChoices


class InformatieCategorie(OrderedModel):
    identifier = models.URLField(_("Identifier"), max_length=255, unique=True)
    name = models.CharField(_("Name"), max_length=80)
    name_plural = models.CharField(_("Name plural"), max_length=80)
    definition = models.TextField(_("Definition"), blank=True)
    origin = models.CharField(
        _("Origin"),
        choices=InformatieCategorieChoices.choices,
        blank=False,
        max_length=15,
    )

    class Meta:
        verbose_name = _("informatie categorie")
        verbose_name_plural = _("informatie categorieën")
        ordering = ("order",)

    def save(self, **kwargs):
        if not self.origin:
            self.origin = InformatieCategorieChoices.zelf_toegevoegd
        return super().save(**kwargs)

    def __str__(self):
        return self.identifier
