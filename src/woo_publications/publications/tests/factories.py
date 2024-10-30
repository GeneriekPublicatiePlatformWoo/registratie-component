import factory

from woo_publications.contrib.documents_api.tests.factories import ServiceFactory

from ..models import Document, Publication


class PublicationFactory(factory.django.DjangoModelFactory):
    officiele_titel = factory.Faker("word")

    class Meta:  # type: ignore
        model = Publication

    @factory.post_generation
    def informatie_categorieen(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for information_category in extracted:
                self.informatie_categorieen.add(information_category)


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
                for_documents_api_docker_compose=True,
            ),
            document_uuid=factory.Faker("uuid4"),
        )
