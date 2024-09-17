from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from woo_publications.api.constants import InformatieCategorieChoices
from woo_publications.api.models import InformatieCategorie


@admin.register(InformatieCategorie)
class InformatieCategorieAdmin(OrderedModelAdmin):
    list_display = ("identifier", "name", "order", "move_up_down_links")
    readonly_fields = ("identifier",)
    search_fields = (
        "identifier",
        "name",
    )
    list_filter = ("origin",)

    def has_change_permission(self, request, obj=None):
        if obj and obj.origin == InformatieCategorieChoices.waardelijst:
            return False
        return True
