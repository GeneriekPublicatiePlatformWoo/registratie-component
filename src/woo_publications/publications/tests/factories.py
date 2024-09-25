import factory

from ..models import Publication


class PublicationFactory(factory.django.DjangoModelFactory):
    officiele_titel = factory.Faker("word")

    class Meta:  # type: ignore
        model = Publication
