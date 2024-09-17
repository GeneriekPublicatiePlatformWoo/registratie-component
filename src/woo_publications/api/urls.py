from django.urls import include, path, re_path
from django.views.generic import RedirectView

from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView
from rest_framework import routers

from .views.category import InformatieCategorieViewset

app_name = "api"

router = routers.DefaultRouter()
router.include_root_view = False

router.register("informatie-categorie", InformatieCategorieViewset)

urlpatterns = [
    path("docs/", RedirectView.as_view(pattern_name="api:api-docs")),
    re_path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
                path(
                    "",
                    SpectacularJSONAPIView.as_view(schema=None),
                    name="api-schema-json",
                ),
                path(
                    "docs/",
                    SpectacularRedocView.as_view(url_name="api:api-schema-json"),
                    name="api-docs",
                ),
            ]
        ),
    ),
]
