import factory

from ..models import InformationCategory, Organisation, Theme


class InformationCategoryFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # pyright: ignore
        model = InformationCategory


class ThemeFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # pyright: ignore
        model = Theme

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # defer creation to treebeard instead of fuzzing the underlying DB fields
        parent = kwargs.pop("parent", None)
        if parent is not None:
            return parent.add_child(**kwargs)  # noqa
        return model_class.add_root(**kwargs)  # noqa


class OrganisationFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # pyright: ignore
        model = Organisation
