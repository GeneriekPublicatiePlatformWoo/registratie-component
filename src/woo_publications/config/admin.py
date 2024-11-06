from django.contrib import admin

from solo.admin import SingletonModelAdmin

from woo_publications.logging.service import AdminAuditLogMixin

from .models import GlobalConfiguration


# FIXME: mixin order messes with singleton admin change_view override
@admin.register(GlobalConfiguration)
class GlobalConfigurationAdmin(AdminAuditLogMixin, SingletonModelAdmin):
    pass
