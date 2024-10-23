import factory
from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.test.factories import ServiceFactory

from ..models import Document, Publication


class PublicationFactory(factory.django.DjangoModelFactory):
    officiele_titel = factory.Faker("word")

    class Meta:  # type: ignore
        model = Publication


class DocumentFactory(factory.django.DjangoModelFactory):
    publicatie = factory.SubFactory(PublicationFactory)
    identifier = factory.Sequence(lambda n: f"document-{n}")
    officiele_titel = factory.Faker("word")
    creatiedatum = factory.Faker("past_date")

    class Meta:  # type: ignore
        model = Document

    class Params:
        with_registered_document = factory.Trait(
            # Configured against the Open Zaak in our docker-compose.yml.
            # See the fixtures in docker/open-zaak.
            document_service=factory.SubFactory(
                ServiceFactory,
                api_root="http://openzaak.docker.internal:8001/documenten/api/v1/",
                api_type=APITypes.drc,
                client_id="woo-publications-dev",
                Secret="insecure-yQL9Rzh4eHGVmYx5w3J2gu",
                auth_type=AuthTypes.zgw,
            ),
            document_uuid=factory.Faker("uuid4"),
        )
