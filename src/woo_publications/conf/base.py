from django.utils.translation import gettext_lazy as _

from open_api_framework.conf.base import *  # noqa
from vng_api_common.conf.api import BASE_REST_FRAMEWORK

from .utils import config

init_sentry()


TIME_ZONE = "Europe/Amsterdam"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS.remove("django.contrib.sites")

INSTALLED_APPS = INSTALLED_APPS + [
    # External applications.
    "capture_tag",
    "hijack",
    "hijack.contrib.admin",
    "timeline_logger",
    "treebeard",
    # Project applications.
    "woo_publications.accounts",
    "woo_publications.api",
    "woo_publications.logging",
    "woo_publications.metadata",
    "woo_publications.publications",
    "woo_publications.utils",
]

INSTALLED_APPS.remove("vng_api_common")
INSTALLED_APPS.remove("notifications_api_common")

MIDDLEWARE = MIDDLEWARE + [
    "hijack.middleware.HijackUserMiddleware",
]

#
# SECURITY settings
#

CSRF_FAILURE_VIEW = "woo_publications.accounts.views.csrf_failure"

#
# Custom settings
#
PROJECT_NAME = _("WOO Publications")
ENABLE_ADMIN_NAV_SIDEBAR = config("ENABLE_ADMIN_NAV_SIDEBAR", default=False)

# Displaying environment information
ENVIRONMENT_LABEL = config("ENVIRONMENT_LABEL", ENVIRONMENT)
ENVIRONMENT_BACKGROUND_COLOR = config("ENVIRONMENT_BACKGROUND_COLOR", "orange")
ENVIRONMENT_FOREGROUND_COLOR = config("ENVIRONMENT_FOREGROUND_COLOR", "black")
SHOW_ENVIRONMENT = config("SHOW_ENVIRONMENT", default=True)

# This setting is used by the csrf_failure view (accounts app).
# You can specify any path that should match the request.path
# Note: the LOGIN_URL Django setting is not used because you could have
# multiple login urls defined.
LOGIN_URLS = [reverse_lazy("admin:login")]

# Default (connection timeout, read timeout) for the requests library (in seconds)
REQUESTS_DEFAULT_TIMEOUT = (10, 30)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# Django-Admin-Index
#
ADMIN_INDEX_SHOW_REMAINING_APPS = False
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = True
ADMIN_INDEX_DISPLAY_DROP_DOWN_MENU_CONDITION_FUNCTION = (
    "woo_publications.utils.django_two_factor_auth.should_display_dropdown_menu"
)

#
# DJANGO-AXES
#
# The number of login attempts allowed before a record is created for the
# failed logins. Default: 3
AXES_FAILURE_LIMIT = 10
# If set, defines a period of inactivity after which old failed login attempts
# will be forgotten. Can be set to a python timedelta object or an integer. If
# an integer, will be interpreted as a number of hours. Default: None
AXES_COOLOFF_TIME = 1

#
# MAYKIN-2FA
#
# It uses django-two-factor-auth under the hood so you can configure
# those settings too.
#
# we run the admin site monkeypatch instead.
# Relying Party name for WebAuthn (hardware tokens)
TWO_FACTOR_WEBAUTHN_RP_NAME = f"WOO Publications ({ENVIRONMENT})"


#
# DJANGO-HIJACK
#
HIJACK_PERMISSION_CHECK = "maykin_2fa.hijack.superusers_only_and_is_verified"
HIJACK_INSERT_BEFORE = (
    '<div class="content">'  # note that this only applies to the admin
)

# Subpath (optional)
# This environment variable can be configured during deployment.
SUBPATH = config("SUBPATH", default="")
if SUBPATH:
    SUBPATH = f"/{SUBPATH.strip('/')}"

#
# DJANGO REST FRAMEWORK
#

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"] = (
    "django_filters.rest_framework.DjangoFilterBackend",
)
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = (
    "rest_framework.pagination.PageNumberPagination"
)
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "woo_publications.api.permissions.AuditHeaderPermission",
)
REST_FRAMEWORK["EXCEPTION_HANDLER"] = "rest_framework.views.exception_handler"

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "TITLE": "WOO Publications",
    "DESCRIPTION": "WIP",
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "SERVE_INCLUDE_SCHEMA": False,
    "CAMELIZE_NAMES": True,
    "TOS": None,
    "CONTACT": {
        "url": "https://github.com/GeneriekPublicatiePlatformWoo/registratie-component",
        "email": "support@maykinmedia.nl",
    },
    "LICENSE": {
        "name": "EUPL",
        "url": "https://github.com/GeneriekPublicatiePlatformWoo/registratie-component/blob/main/LICENSE.md",
    },
    "VERSION": "0.1.0",
    "TAGS": [],
    "EXTERNAL_DOCS": {
        "description": "Functional and technical documentation",
        "url": "https://odrc.readthedocs.io/",
    },
}

#
# ZGW-CONSUMERS
#
ZGW_CONSUMERS_IGNORE_OAS_FIELDS = True
