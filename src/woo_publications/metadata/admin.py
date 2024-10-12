from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ..logging import AdminAuditLogMixin
from .constants import InformationCategoryOrigins
from .models import InformationCategory, Theme


@admin.register(InformationCategory)
class InformationCategoryAdmin(AdminAuditLogMixin, OrderedModelAdmin):
    list_display = ("naam", "identifier", "oorsprong", "move_up_down_links")
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


@admin.register(Theme)
class ThemeAdmin(
    AdminAuditLogMixin, TreeAdmin
):  # use Model admin because nothing should be editable anyway
    list_display = ("naam", "identifier")
    search_fields = ("identifier", "naam")
    form = movenodeform_factory(Theme)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
