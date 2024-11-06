from typing import Sequence

import factory

from woo_publications.contrib.documents_api.tests.factories import ServiceFactory
from woo_publications.metadata.models import InformationCategory
from woo_publications.metadata.tests.factories import OrganisationFactory

from ..models import Document, Publication


class PublicationFactory(factory.django.DjangoModelFactory):
    publisher = factory.SubFactory(OrganisationFactory, is_actief=True)
    officiele_titel = factory.Faker("word")

    class Meta:  # pyright: ignore
        model = Publication

    @factory.post_generation
    def informatie_categorieen(
        obj: Publication,  # pyright: ignore reportGeneralTypeIssues
        create: bool,
        extracted: Sequence[InformationCategory],
        **kwargs,
    ):
        if not create:
            return

        if extracted:
            obj.informatie_categorieen.set(extracted)


class DocumentFactory(factory.django.DjangoModelFactory):
    publicatie = factory.SubFactory(PublicationFactory)
    identifier = factory.Sequence(lambda n: f"document-{n}")
    officiele_titel = factory.Faker("word")
    creatiedatum = factory.Faker("past_date")

    class Meta:  # pyright: ignore
        model = Document

    class Params:
        with_registered_document = factory.Trait(
            # Configured against the Open Zaak in our docker-compose.yml.
            # See the fixtures in docker/open-zaak.
            document_service=factory.SubFactory(
                ServiceFactory,
                for_documents_api_docker_compose=True,
            ),
            document_uuid=factory.Faker("uuid4"),
        )
