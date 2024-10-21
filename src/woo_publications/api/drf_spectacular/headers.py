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

ALL_AUDIT_PARAMETERS = [
    AUDIT_USER_REPRESENTATION_PARAMETER,
    AUDIT_USER_ID_PARAMETER,
    AUDIT_REMARKS_PARAMETER,
]
