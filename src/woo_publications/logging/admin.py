from django.contrib import admin

from timeline_logger.models import TimelineLog

admin.site.unregister(TimelineLog)
