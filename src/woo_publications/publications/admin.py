from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from furl import furl

from .models import Document, Publication


class DocumentInlineAdmin(admin.StackedInline):
    model = Document
    extra = 0


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        "officiele_titel",
        "verkorte_titel",
        "registratiedatum",
        "uuid",
        "show_actions",
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
    inlines = (DocumentInlineAdmin,)

    @admin.display(description=_("actions"))
    def show_actions(self, obj: Publication) -> str:
        actions = [
            (
                furl(reverse("admin:publications_document_changelist")).add(
                    {"publicatie__exact": obj.pk}
                ),
                _("Show documents"),
            )
        ]
        return format_html_join(
            " | ",
            '<a href="{}">{}</a>',
            actions,
        )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "officiele_titel",
        "verkorte_titel",
        "bestandsnaam",
        "show_filesize",
        "identifier",
        "registratiedatum",
    )
    search_fields = (
        "identifier",
        "officiele_titel",
        "verkorte_titel",
        "bestandsnaam",
        "publicatie__uuid",
    )
    list_filter = ("registratiedatum", "creatiedatum")
    date_hierarchy = "registratiedatum"

    @admin.display(description=_("file size"), ordering="bestandsomvang")
    def show_filesize(self, obj: Document) -> str:
        return filesizeformat(obj.bestandsomvang)