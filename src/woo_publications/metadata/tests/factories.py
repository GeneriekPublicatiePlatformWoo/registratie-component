import factory

from ..models import InformatieCategorie


class InformatieCategorieFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:
        model = InformatieCategorie
