import re

from djangorestframework_camel_case.util import (
    underscore_to_camel as _underscore_to_camel,
)

RE_UNDERSCORE = re.compile(r"[a-z]_[a-z]")


def underscore_to_camel[T: str | int](input_: T) -> T:
    """
    Convert a string from under_score to camelCase.
    """
    if not isinstance(input_, str):
        return input_

    return re.sub(RE_UNDERSCORE, _underscore_to_camel, input_)
