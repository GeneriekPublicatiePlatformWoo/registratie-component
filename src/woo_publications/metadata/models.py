from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel

from .constants import InformatieCategorieOrigins


class InformatieCategorie(OrderedModel):
    identifier = models.URLField(
        _("identifier"),
        help_text=_(
            "The unique IRI that identifies this category in the overheid.nl value list. "
            "For entries that have been added manually, an identifier is generated."
        ),
        max_length=255,
        unique=True,
    )
    naam = models.CharField(
        _("name"),
        help_text=_("The name of the category."),
        max_length=80,
    )
    naam_meervoud = models.CharField(
        _("name plural"),
        help_text=_("The plural name of the category."),
        max_length=80,
        blank=True,
    )
    definitie = models.TextField(
        _("definition"),
        help_text=_("The description of the category."),
        blank=True,
    )
    oorsprong = models.CharField(
        _("origin"),
        help_text=_(
            "Determines where the category is defined and sourced from, and how "
            "the identifier should be interpreted. If the value list is the origin, the "
            "category can not be modified or deleted."
        ),
        choices=InformatieCategorieOrigins.choices,
        blank=False,
        max_length=15,
        default=InformatieCategorieOrigins.custom_entry,
    )

    class Meta(OrderedModel.Meta):
        verbose_name = _("information category")
        verbose_name_plural = _("information categories")

    def __str__(self):
        return self.naam
