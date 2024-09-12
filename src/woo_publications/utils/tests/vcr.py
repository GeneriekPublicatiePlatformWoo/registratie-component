import os
from pathlib import Path

from vcr.unittest import VCRMixin

RECORD_MODE = os.environ.get("VCR_RECORD_MODE", "none")


class VCRMixin(VCRMixin):
    """
    Mixin to use VCR in your unit tests.

    Using this mixin will result in HTTP requests/responses being recorded.
    """

    def _get_cassette_library_dir(self):
        split_path = str(self.__class__.__module__).split(".")
        test_dir = split_path.pop()
        path = Path("/".join(split_path))
        class_name = self.__class__.__qualname__
        return str("src" / path / "vcr_cassettes" / test_dir / class_name)

    def _get_cassette_name(self):
        return f"{self._testMethodName}.yaml"

    def _get_vcr_kwargs(self):
        kwargs = super()._get_vcr_kwargs()
        kwargs.setdefault("record_mode", RECORD_MODE)
        return kwargs
