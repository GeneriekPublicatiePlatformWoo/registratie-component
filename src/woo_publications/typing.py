from typing import TypedDict

type JSONPrimitive = str | int | float | bool | None
type JSONValue = JSONPrimitive | JSONObject | list[JSONValue]
type JSONObject = dict[str, JSONValue]

ApiUser = TypedDict("ApiUser", {"user_id": str, "user_repr": str})
