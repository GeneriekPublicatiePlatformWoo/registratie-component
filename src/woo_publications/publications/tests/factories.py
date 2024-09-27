import factory

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
