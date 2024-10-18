from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Origins(TextChoices):
    value_list = "waardelijst", _("Value list")
    custom_entry = "zelf_toegevoegd", _("Custom entry")
