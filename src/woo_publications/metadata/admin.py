from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .constants import InformationCategoryOrigins
from .models import InformationCategory


@admin.register(InformationCategory)
class InformationCategoryAdmin(OrderedModelAdmin):
    list_display = ("naam", "identifier", "oorsprong", "move_up_down_links")
    readonly_fields = ("oorsprong",)
    search_fields = (
        "identifier",
        "naam",
    )
    list_filter = ("oorsprong",)

    def has_change_permission(self, request, obj=None):
        if obj and obj.oorsprong == InformationCategoryOrigins.value_list:
            return False
        return True
