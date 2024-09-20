from drf_spectacular.contrib.django_filters import DjangoFilterExtension

from woo_publications.api.utils import underscore_to_camel


class CamelizeFilterExtension(DjangoFilterExtension):
    priority = 1

    def get_schema_operation_parameters(self, auto_schema, *args, **kwargs):
        """
        camelize query parameters
        """
        parameters = super().get_schema_operation_parameters(  # pragma: no cover
            auto_schema, *args, **kwargs
        )

        for parameter in parameters:
            parameter["name"] = underscore_to_camel(
                parameter["name"]
            )  # pragma: no cover

        return parameters  # pragma: no cover
