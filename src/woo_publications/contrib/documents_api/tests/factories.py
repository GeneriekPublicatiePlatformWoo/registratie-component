import factory
from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.test.factories import ServiceFactory as _ServiceFactory


class ServiceFactory(_ServiceFactory):
    class Params:  # type: ignore
        # See ``docker/open-zaak/README.md`` for the test credentials and available
        # data.
        for_documents_api_docker_compose = factory.Trait(
            label="Open Zaak (docker-compose)",
            api_root="http://openzaak.docker.internal:8001/documenten/api/v1/",
            api_type=APITypes.drc,
            auth_type=AuthTypes.zgw,
            client_id="woo-publications-dev",
            secret="insecure-yQL9Rzh4eHGVmYx5w3J2gu",
        )
