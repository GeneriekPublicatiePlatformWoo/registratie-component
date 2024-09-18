import inspect
import os
from pathlib import Path

from vcr.unittest import VCRMixin

RECORD_MODE = os.environ.get("VCR_RECORD_MODE", "none")


class VCRMixin(VCRMixin):
    """
    Mixin to use VCR in your unit tests.

    Using this mixin will result in HTTP requests/responses being recorded.
    """

    _testMethodName: str

    def _get_cassette_library_dir(self):
        class_name = self.__class__.__qualname__
        path = Path(inspect.getfile(self.__class__))
        return str(path.parent / "vcr_cassettes" / path.stem / class_name)

    def _get_cassette_name(self):
        return f"{self._testMethodName}.yaml"

    def _get_vcr_kwargs(self, **kwargs):
        kwargs.setdefault("record_mode", RECORD_MODE)
        return kwargs
