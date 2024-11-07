from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import GlobalConfiguration


@admin.register(GlobalConfiguration)
class GlobalConfigurationAdmin(SingletonModelAdmin):
    pass
