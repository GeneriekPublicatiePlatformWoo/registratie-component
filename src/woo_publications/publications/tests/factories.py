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
        document_service_configured = factory.Trait(
            document_service=factory.SubFactory(
                ServiceFactory,
                api_root="https://example.com/",
                api_type=APITypes.drc,
                oas="https://example.com/api/v1/oas",
                header_key="Authorization",
                header_value="Token 0cbccf9e-f9cd-4f9c-9516-7481e79989df",
                auth_type=AuthTypes.api_key,
            ),
            document_uuid=factory.Faker("uuid4"),
        )
