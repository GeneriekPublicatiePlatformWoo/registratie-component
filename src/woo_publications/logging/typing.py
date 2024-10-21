from typing import NotRequired, TypedDict


class ActingUser(TypedDict):
    identifier: int | str
    display_name: str


class MetadataDict(TypedDict):
    """
    Optimistic model for the metadata - unfortunately we can't add DB constraints.
    """

    event: str
    acting_user: ActingUser
    _cached_object_repr: NotRequired[str]
