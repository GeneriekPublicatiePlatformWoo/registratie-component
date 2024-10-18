from drf_spectacular.plumbing import build_parameter_type
from drf_spectacular.utils import OpenApiParameter

AUDIT_USER_REPRESENTATION_PARAMETER = build_parameter_type(
    name="Audit-User-Representation",
    schema={"type": "string"},
    location=OpenApiParameter.HEADER,
    required=True,
)
AUDIT_USER_ID_PARAMETER = build_parameter_type(
    name="Audit-User-ID",
    schema={"type": "string"},
    location=OpenApiParameter.HEADER,
    required=True,
)
AUDIT_REMARKS_PARAMETER = build_parameter_type(
    name="Audit-Remarks",
    schema={"type": "string"},
    location=OpenApiParameter.HEADER,
    required=True,
)


def add_log_parameter(result, generator, request, public):
    for path in result["paths"].values():
        for operation_method, operation in path.items():
            operation.setdefault("parameters", [])
            operation["parameters"].append(AUDIT_USER_REPRESENTATION_PARAMETER)
            operation["parameters"].append(AUDIT_USER_ID_PARAMETER)
            operation["parameters"].append(AUDIT_REMARKS_PARAMETER)

    return result
