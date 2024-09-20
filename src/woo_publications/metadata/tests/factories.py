import factory

from ..models import InformationCategory, Theme


class InformationCategoryFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # type: ignore
        model = InformationCategory


class ThemeFactory(factory.django.DjangoModelFactory):
    naam = factory.Faker("word")

    class Meta:  # type: ignore
        model = Theme

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # defer creation to treebeard instead of fuzzing the underlying DB fields
        parent = kwargs.pop("parent", None)
        if parent is not None:
            return parent.add_child(**kwargs)  # noqa
        return model_class.add_root(**kwargs)  # noqa
