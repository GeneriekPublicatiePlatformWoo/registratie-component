from django.db import models
from django.utils.translation import gettext_lazy as _


class PublicationStatusOptions(models.TextChoices):
    published = "gepubliceerd", _("Published")
    concept = "concept", _("Concept")
    revoked = "ingetrokken", _("Revoked")
