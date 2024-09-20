import factory

from ..models import InformationCategory


class InformationCategoryFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # type: ignore
        model = InformationCategory
