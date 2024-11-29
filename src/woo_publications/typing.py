type JSONPrimitive = str | int | float | bool | None
type JSONValue = JSONPrimitive | JSONObject | list[JSONValue]
type JSONObject = dict[str, JSONValue]
type JSON = list[JSONObject]
