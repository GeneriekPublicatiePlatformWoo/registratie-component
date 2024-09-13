from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InformatieCategorieChoices(TextChoices):
    waardelijst = "waardelijst", _("Waardelijst")
    zelf_toegevoegd = "zelf_toegevoegd", _("Zelf toegevoegd")
