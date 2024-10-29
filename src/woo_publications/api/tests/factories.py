import factory

from ..constants import PermissionOptions
from ..models import TokenAuth


class TokenAuthFactory(factory.django.DjangoModelFactory):
    permissies = []

    class Meta:  # type: ignore
        model = TokenAuth

    class Params:
        read_permission = factory.Trait(permissies=[PermissionOptions.read.value])
        write_permission = factory.Trait(permissies=[PermissionOptions.write.value])
        read_write_permission = factory.Trait(
            permissies=[
                PermissionOptions.read.value,
                PermissionOptions.write.value,
            ]
        )
