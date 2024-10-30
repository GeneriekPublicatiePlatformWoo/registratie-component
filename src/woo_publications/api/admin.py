from django.contrib import admin

from woo_publications.logging.admin_tools import AdminAuditLogMixin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(AdminAuditLogMixin, admin.ModelAdmin):
    list_display = ("token", "contact_person", "email", "phone_number", "created")
    readonly_fields = ("token",)
