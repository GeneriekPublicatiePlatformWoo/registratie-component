from vng_api_common.conf.api import *  # noqa

# DRF
REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK["PAGE_SIZE"] = 100
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = (
    "vng_api_common.pagination.DynamicPageSizePagination"
)
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"

SPECTACULAR_SETTINGS = {
    "SERVE_INCLUDE_SCHEMA": False,
    "CAMELIZE_NAMES": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "TITLE": "WOO Publications",
    "DESCRIPTION": "WIP",
    "CONTACT": {
        "url": "https://github.com/GeneriekPublicatiePlatformWoo/registratie-component",
    },
    "LICENSE": {
        "name": "EUPL",
        "url": "https://github.com/GeneriekPublicatiePlatformWoo/registratie-component/blob/main/LICENSE.md",
    },
}
