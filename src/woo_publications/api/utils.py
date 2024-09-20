import re

from djangorestframework_camel_case.util import (
    camelize_re,
    underscore_to_camel as _underscore_to_camel,
)


def underscore_to_camel[T: str | int](input_: T) -> T:
    """
    Convert a string from under_score to camelCase.
    """
    if not isinstance(input_, str):
        return input_

    return re.sub(camelize_re, _underscore_to_camel, input_)
