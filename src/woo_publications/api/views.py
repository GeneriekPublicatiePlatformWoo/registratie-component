from django.conf import settings
from django.shortcuts import redirect


def redirect_to_schema_view(request):
    return redirect("schema-redoc", version=settings.REST_FRAMEWORK["DEFAULT_VERSION"])
