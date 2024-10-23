from django.db.models import Manager

from ordered_model.models import OrderedModelManager
from treebeard.mp_tree import MP_NodeManager


class ThemeManager(MP_NodeManager):
    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class OrganisationManager(Manager):
    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class InformationCategoryManager(OrderedModelManager):
    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)
