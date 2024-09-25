from django.contrib import admin

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        "officiele_titel",
        "verkorte_titel",
        "registratiedatum",
        "uuid",
    )
    readonly_fields = (
        "uuid",
        "registratiedatum",
    )
    search_fields = (
        "uuid",
        "officiele_titel",
        "verkorte_titel",
    )
    list_filter = ("registratiedatum",)
    date_hierarchy = "registratiedatum"
