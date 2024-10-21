from itertools import chain

from django.db import models


def model_to_dict(instance, fields=None, exclude=None):
    """
    Modified version of django.forms.model_to_dict which doesn't skip non-editable fields.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def serialize_instance(instance: models.Model):
    return model_to_dict(instance)
