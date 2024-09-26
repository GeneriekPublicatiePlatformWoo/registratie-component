import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel
from treebeard.mp_tree import MP_Node

from .constants import InformationCategoryOrigins

CUSTOM_CATEGORY_IDENTIFIER_URL_PREFIX = (
    "https://generiek-publicatieplatform.woo/informatiecategorie/"
)

CUSTOM_THEME_URL_PREFIX = "https://generiek-publicatieplatform.woo/thema/"


def get_default_information_category_identifier():
    return f"{CUSTOM_CATEGORY_IDENTIFIER_URL_PREFIX}{uuid.uuid4()}"


def get_default_theme_identifier():
    return f"{CUSTOM_THEME_URL_PREFIX}{uuid.uuid4()}"


class InformationCategory(OrderedModel):
    uuid = models.UUIDField(_("UUID"), unique=True, default=uuid.uuid4)
    identifier = models.URLField(
        _("identifier"),
        help_text=_(
            "The unique IRI that identifies this category in the overheid.nl value list. "
            "For entries that have been added manually, an identifier is generated."
        ),
        max_length=255,
        unique=True,
        editable=False,
        default=get_default_information_category_identifier,
    )
    naam = models.CharField(_("name"), max_length=80)
    naam_meervoud = models.CharField(_("name plural"), max_length=80, blank=True)
    definitie = models.TextField(_("definition"), blank=True)
    oorsprong = models.CharField(
        _("origin"),
        help_text=_(
            "Determines where the category is defined and sourced from, and how "
            "the identifier should be interpreted. If the value list is the origin, the "
            "category can not be modified or deleted."
        ),
        choices=InformationCategoryOrigins.choices,
        blank=False,
        max_length=15,
        default=InformationCategoryOrigins.custom_entry,
    )

    class Meta(OrderedModel.Meta):
        verbose_name = _("information category")
        verbose_name_plural = _("information categories")

    def __str__(self):
        return self.naam


class Theme(MP_Node):
    uuid = models.UUIDField(_("UUID"), unique=True, default=uuid.uuid4)
    identifier = models.URLField(
        _("identifier"),
        help_text=_(
            "The unique IRI that identifies this theme in the overheid.nl value list. "
            "For entries that have been added manually, an identifier is generated."
        ),
        max_length=255,
        unique=True,
        editable=False,
        default=get_default_theme_identifier,
    )
    naam = models.CharField(_("name"), max_length=80)

    node_order_by = ("naam",)

    class Meta:  # type: ignore
        verbose_name = _("theme")
        verbose_name_plural = _("themes")

    def __str__(self):
        return self.naam
