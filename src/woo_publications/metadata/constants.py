from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InformationCategoryOrigins(TextChoices):
    value_list = "waardelijst", _("Value list")
    custom_entry = "zelf_toegevoegd", _("Custom entry")


class OrganisationActive(TextChoices):
    active = "true", _("Retrieves all the active organisations (default)")
    inactive = "false", _("Retrieves all the inactive organisations")
    all = "alle", _("Retrieve every organisation regardless if active or inactive.")


class OrganisationOrigins(TextChoices):
    municipality_list = "gemeentelijst", _("Municipality list")
    so_list = "solijst", _("Collaborative organisations list")
    oorg_list = "oorglijst", _("Alternative government organisations")
    custom_entry = "zelf_toegevoegd", _("Custom entry")
