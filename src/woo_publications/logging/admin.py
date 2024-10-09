from django.contrib import admin
from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext, gettext_lazy as _

from timeline_logger.models import TimelineLog

from .constants import Events
from .models import TimelineLogProxy

admin.site.unregister(TimelineLog)


@admin.register(TimelineLogProxy)
class TimelineLogProxyAdmin(admin.ModelAdmin):
    list_display = (
        "message",
        "show_event",
        "timestamp",
        "show_acting_user",
        "content_admin_link",
    )
    # TODO: add filters/search on event and acting user
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
    search_fields = (
        "extra_data__acting_user__identifier",
        "extra_data__acting_user__display_name",
    )
    list_select_related = ("content_type", "user")
    date_hierarchy = "timestamp"
    readonly_fields = ("get_message",)

    def has_add_permission(self, request: HttpRequest):
        # Not even superusers are allowed to make changes
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: TimelineLogProxy | None = None
    ):
        # Not even superusers are allowed to make changes
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: TimelineLogProxy | None = None
    ):
        # Not even superusers are allowed to make changes
        return False

    @admin.display(description=_("full log message"))
    def full_message(self, obj: TimelineLogProxy) -> str:
        return obj.get_message()

    @admin.display(description=_("message"))
    def message(self, obj: TimelineLogProxy) -> str:
        full_msg = strip_tags(self.full_message(obj))
        return Truncator(full_msg).chars(100) or gettext("(no message)")

    @admin.display(description=_("event"), ordering="extra_data__event")
    def show_event(self, obj: TimelineLogProxy) -> str:
        if (event := obj.event) == "unknown":
            return gettext("Unknown")
        return Events(event).label

    @admin.display(description=_("acting user"))
    def show_acting_user(self, obj: TimelineLogProxy) -> str:
        acting_user, django_user = obj.acting_user
        format_str = (
            gettext("{name} ({identifier})")
            if not django_user
            else gettext("{name} ({identifier}, local user ID: {django_id})")
        )
        return format_str.format(
            name=acting_user["display_name"],
            identifier=acting_user["identifier"],
            django_id=django_user.pk if django_user else None,
        )

    @admin.display(description=_("affected object"))
    def content_admin_link(self, obj: TimelineLogProxy) -> str:
        if not (obj.object_id and obj.content_type_id):
            return "-"
        ct = obj.content_type
        try:
            admin_path = reverse(
                f"admin:{ct.app_label}_{ct.model}_change", args=(obj.object_id,)
            )
        except NoReverseMatch:  # content type not enabled in the admin
            return "-"
        return format_html(
            '<a href="{u}">{t}</a>', u=admin_path, t=str(obj.content_object)
        )
