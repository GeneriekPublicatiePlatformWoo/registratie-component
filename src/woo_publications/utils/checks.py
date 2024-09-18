import os
import socket

from django.conf import settings
from django.core.checks import Error, Warning, register
from django.forms import ModelForm


def get_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


@register()
def check_modelform_exclude(app_configs, **kwargs):
    """
    Check that ModelForms use Meta.fields instead of Meta.exclude.

    ModelForm.Meta.exclude is dangerous because it doesn't protect against
    fields that are added later. Explicit white-listing is safer and prevents
    bugs such as IMA #645.

    This check piggy-backs on all form modules to be imported during Django
    startup. It won't cover forms that are defined on the fly such as in
    formset factories.
    """
    errors = []

    for form in get_subclasses(ModelForm):
        # ok, fields is defined
        if form._meta.fields or getattr(form.Meta, "fields", None):
            continue

        # no `.fields` defined, so scream loud enough to prevent this
        errors.append(
            Error(
                "ModelForm %s.%s with Meta.exclude detected, this is a bad practice"
                % (form.__module__, form.__name__),
                hint="Use ModelForm.Meta.fields instead",
                obj=form,
                id="utils.E001",
            )
        )

    return errors


@register
def check_missing_init_files(app_configs, **kwargs):
    """
    Check that all packages have __init__.py files.

    If they don't, the code will still run, but tests aren't picked up by the
    test runner, for example.
    """
    errors = []

    for dirpath, dirnames, filenames in os.walk(settings.DJANGO_PROJECT_DIR):
        dirname = os.path.split(dirpath)[1]
        if dirname == "__pycache__":
            continue

        if "__init__.py" in filenames:
            continue

        extensions = [os.path.splitext(fn)[1] for fn in filenames]
        if ".py" not in extensions:
            continue

        errors.append(
            Warning(
                "Directory %s does not contain an `__init__.py` file" % dirpath
                + dirname,
                hint="Consider adding this module to make sure tests are picked up",
                id="utils.W001",
            )
        )

    return errors


@register
def check_docker_hostname_dns(app_configs, **kwargs):
    """
    Check that the host.internal.docker hostname resolves to an IP address.

    For simplicity sake we will program interaction tests on this hostname - this
    requires developers (and CI environments) to have their /etc/hosts configured
    properly though, otherwise they'll get weird and hard-to-understand test failures.
    """
    warnings = []

    try:
        socket.gethostbyname("host.docker.internal")
    except socket.gaierror:  # pragma: no cover
        warnings.append(
            Warning(
                "Could not resolve host.internal.docker to an IP address (expecting "
                "127.0.0.1). This will result in test failures.",
                hint=(
                    "Add the line '127.0.0.1 host.docker.internal' to your /etc/hosts "
                    "file."
                ),
                id="utils.W002",
            )
        )

    return warnings
