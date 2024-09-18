from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .constants import InformatieCategorieOrigins
from .models import InformatieCategorie


@admin.register(InformatieCategorie)
class InformatieCategorieAdmin(OrderedModelAdmin):
    list_display = ("identifier", "naam", "order", "move_up_down_links")
    readonly_fields = ("oorsprong",)
    search_fields = (
        "identifier",
        "naam",
    )
    list_filter = ("oorsprong",)

    def has_change_permission(self, request, obj=None):
        if obj and obj.oorsprong == InformatieCategorieOrigins.value_list:
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj and obj.oorsprong == InformatieCategorieOrigins.custom_entry:
            readonly_fields += ("identifier",)

        return readonly_fields
