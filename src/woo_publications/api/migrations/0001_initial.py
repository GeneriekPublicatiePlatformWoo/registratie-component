# Generated by Django 4.2.16 on 2024-10-30 17:06

from django.db import migrations, models
import django_jsonform.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=40, verbose_name="token")),
                (
                    "permissions",
                    django_jsonform.models.fields.ArrayField(  # type: ignore reportArgumentType
                        base_field=models.CharField(
                            choices=[("read", "Read"), ("write", "Write")],
                            max_length=20,
                        ),
                        blank=True,
                        default=list,
                        help_text="The permissions this API token has access to.",
                        size=None,
                        verbose_name="permissions",
                    ),
                ),
                (
                    "contact_person",
                    models.CharField(
                        blank=True,
                        help_text="Name of the person to contact about this application and the associated credentials.",
                        max_length=200,
                        verbose_name="contact person",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        help_text="Email of the person to contact about this application and the associated credentials.",
                        max_length=254,
                        verbose_name="email",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Phonenumber of the person contact about this application and the associated credentials.",
                        max_length=128,
                        region=None,
                        verbose_name="phone number",
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Last date when the token was modified",
                        verbose_name="last modified",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Date when the token was created",
                        verbose_name="created",
                    ),
                ),
            ],
            options={
                "verbose_name": "application API key",
                "verbose_name_plural": "application API keys",
            },
        ),
    ]