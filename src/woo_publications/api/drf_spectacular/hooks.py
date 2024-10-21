from drf_spectacular.utils import _SchemaType
from rest_framework.request import Request
from rest_framework.schemas.generators import BaseSchemaGenerator

from .headers import ALL_AUDIT_PARAMETERS


def add_log_parameter(
    result: _SchemaType,
    generator: BaseSchemaGenerator,
    request: Request | None,
    public: bool,
):
    for path in result["paths"].values():
        for operation in path.values():
            # the paths object may be extended with custom, non-standard extensions
            if "responses" not in operation:  # pragma: no cover
                continue

            operation.setdefault("parameters", [])
            operation["parameters"] += ALL_AUDIT_PARAMETERS

    return result
