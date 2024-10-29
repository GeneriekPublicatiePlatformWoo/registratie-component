import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_jsonform.models.fields import JSONField
from phonenumber_field.modelfields import PhoneNumberField

from .constants import PermissionOptions

PERMISSION_SCHEMA = {
    "type": "list",
    "items": {
        "type": "string",
        "choices": [
            {"title": label, "value": value}
            for value, label in PermissionOptions.choices
        ],
        "widget": "multiselect",
    },
}


class TokenAuth(models.Model):
    token = models.CharField(_("token"), max_length=40, primary_key=True)
    permissies = JSONField(
        _("permission"),
        help_text=_("The permission this API token has access to."),
        schema=PERMISSION_SCHEMA,
        blank=True,
        null=True,
    )
    contact_persoon = models.CharField(
        _("contact person"),
        max_length=200,
        help_text=_("Name of the person who can access the API"),
        blank=True,
    )
    email = models.EmailField(
        _("email"),
        help_text=_("Email of the person, who can access the API"),
        blank=True,
    )
    telefoon_nummer = PhoneNumberField(
        _("phonenumber"),
        help_text=_("Phonenumber of the person, who can access the API"),
        blank=True,
    )
    last_modified = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        help_text=_("Last date when the token was modified"),
    )
    created = models.DateTimeField(
        _("created"), auto_now_add=True, help_text=_("Date when the token was created")
    )

    class Meta:
        verbose_name = _("token authorization")
        verbose_name_plural = _("token authorizations")

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()
