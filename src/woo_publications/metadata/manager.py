from ordered_model.models import OrderedModelManager


class InformationCategoryManager(OrderedModelManager):
    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)
