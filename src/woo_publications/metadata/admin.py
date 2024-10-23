from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from ordered_model.admin import OrderedModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from woo_publications.logging.service import AdminAuditLogMixin, get_logs_link

from .constants import InformationCategoryOrigins
from .models import InformationCategory, Theme


@admin.register(InformationCategory)
class InformationCategoryAdmin(AdminAuditLogMixin, OrderedModelAdmin):
    list_display = (
        "naam",
        "identifier",
        "oorsprong",
        "show_actions",
        "move_up_down_links",
    )
    readonly_fields = (
        "uuid",
        "oorsprong",
    )
    search_fields = (
        "identifier",
        "naam",
    )
    list_filter = ("oorsprong",)

    def has_change_permission(self, request, obj=None):
        if obj and obj.oorsprong == InformationCategoryOrigins.value_list:
            return False
        return True

    @admin.display(description=_("actions"))
    def show_actions(self, obj: InformationCategory) -> str:
        actions = [
            get_logs_link(obj),
        ]
        return format_html_join(
            " | ",
            '<a href="{}">{}</a>',
            actions,
        )


@admin.register(Theme)
class ThemeAdmin(AdminAuditLogMixin, TreeAdmin):
    list_display = ("naam", "identifier", "show_actions")
    search_fields = ("identifier", "naam")
    form = movenodeform_factory(Theme)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description=_("actions"))
    def show_actions(self, obj: Theme) -> str:
        actions = [
            get_logs_link(obj),
        ]
        return format_html_join(
            " | ",
            '<a href="{}">{}</a>',
            actions,
        )
