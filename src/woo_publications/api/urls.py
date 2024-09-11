from django.urls import include, path, re_path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .views import redirect_to_schema_view

router = routers.DefaultRouter()


urlpatterns = [
    re_path(
        r"^v(?P<version>\d+)/",
        include(
            [
                re_path(r"^", include(router.urls)),
                path("", router.APIRootView.as_view(), name="api-root"),
                path(
                    "openapi.yaml",
                    SpectacularYAMLAPIView.as_view(),
                    name="schema-yaml",
                ),
                path(
                    "openapi.json",
                    SpectacularJSONAPIView.as_view(),
                    name="schema-json",
                ),
                path(
                    "docs/",
                    SpectacularRedocView.as_view(url_name="schema-yaml"),
                    name="schema-redoc",
                ),
            ]
        ),
    ),
    path("docs/", redirect_to_schema_view, name="redirect_to_schema"),
]
