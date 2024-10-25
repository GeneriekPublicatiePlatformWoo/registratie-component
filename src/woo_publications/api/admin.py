from django.contrib import admin

from woo_publications.logging.admin_tools import AdminAuditLogMixin

from .models import TokenAuth


@admin.register(TokenAuth)
class TokenAuthAdmin(AdminAuditLogMixin, admin.ModelAdmin):
    list_display = ("token", "contact_persoon", "email", "telefoon_nummer", "created")
    readonly_fields = ("token",)
