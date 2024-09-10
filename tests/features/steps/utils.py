import json
import string
import re
from time import sleep
from typing import Any, Dict, Optional
from behave import when


def table_to_json(context) -> Dict[str, Any]:
    """
    Convert Behave context table to a nested JSON-like dictionary, supporting
    nested dictionaries, arrays, and complex structures.

    The table should have the following structure:

    +----------------------+--------+---------+
    | key                  | value  | type    |
    +----------------------+--------+---------+
    | key1                 | value1 | string  |
    | key2                 | value2 | string  |
    | key3                 | 2      | integer |
    | key4.key5            | value3 | string  |
    | key6[0].toto         | tata   | string  |
    | key6[1].titi         | toto   | string  |
    | key1.key2[0]         | value1 | string  |
    | key1.key2[1].subkey1 | value2 | string  |
    +----------------------+--------+---------+

    The resulting dictionary will have the following structure:

    .. code-block:: json

        {
            "key1": {
                "key2": [
                    "value1",
                    {
                        "subkey1": "value2"
                    }
                ]
            },
            "key2": "value2",
            "key3": 2,
            "key4": {
                "key5": "value3"
            },
            "key6": [
                {
                    "toto": "tata"
                },
                {
                    "titi": "toto"
                }
            ]
        }

    Key features:

    - Supports nested keys using dot notation (e.g., "key4.key5").
    - Supports arrays within the structure using square brackets (e.g., "key6[0].toto").
    - Handles complex structures combining dictionaries and arrays (e.g., "key1.key2[0].subkey1").

    The `type` parameter is used to specify the type of the value in the table, and can be one of the following:
    - `string`: Default type if not specified.
    - `integer`: Converts the value to an integer.
    - `float`: Converts the value to a float.
    - `boolean`: Converts the value to a boolean.
    - `json`: Interprets the value as a JSON object.

    :param context: The context object containing a table attribute, where each row includes a `key`, `value`, and `type`.
    :type context: Any
    :return: A dictionary containing the table data converted to a nested JSON-like structure.
    :rtype: Dict[str, Any]
    """

    data: Dict[str, Any] = {}
    type_converters = {
        "string": str,
        "integer": int,
        "float": float,
        "boolean": bool,
        "json": json.loads,
    }

    for row in context.table:
        key, value, value_type = row["key"], row["value"], row["type"] or "string"
        value = replace_values_in_string(context, value)
        key_parts = key.split(".")
        current = data

        for part in key_parts[:-1]:
            # creation of the nested structure
            current = _handle_nested_keys_and_arrays(current, part)

        final_part = key_parts[-1]
        current = _handle_nested_keys_and_arrays(
            current, final_part, value, value_type, type_converters
        )

    return data


def _handle_nested_keys_and_arrays(
    current: Any,
    part: str,
    value: Optional[str] = None,
    value_type: Optional[str] = None,
    type_converters: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Private helper method to handle keys that may contain arrays or nested dictionaries.

    If the key contains an array index (e.g., "key6[0]"), this method ensures that the corresponding
    part of the structure is a list, and creates or grows the list as needed.

    :param current: The current part of the JSON-like structure being processed (either a dictionary or a list).
    :param part: The key to be processed. Can be a regular key or an array index (e.g., "key6[0]").
    :param value: The value to be inserted, only required if this is the last key part.
    :param value_type: The type of the value, used for type conversion (e.g., "integer", "float").
    :param type_converters: A dictionary of type converters for processing values of different types.
    :return: The updated part of the JSON-like structure.
    :rtype: Any
    """
    array_pattern = re.compile(
        r"(\w+)\[(\d+)\]"
    )  # Pattern to match array keys like key6[0]
    array_match = array_pattern.match(part)

    if array_match:
        array_key, index = array_match.groups()
        index = int(index)
        if array_key not in current:
            current[array_key] = []
        while len(current[array_key]) <= index:
            current[array_key].append({})
        current = current[array_key][index]
    else:  # Not an array
        if value is not None and value_type is not None and type_converters is not None:
            if value_type in type_converters:
                current[part] = type_converters[value_type](value)
            else:
                current[part] = value
        else:
            if part not in current:
                current[part] = {}
            current = current[part]

    return current


def replace_values_in_string(context, string_with_placeholders: str):
    """
    Replaces values in a string with values from the Behave context.

    Parameters:
        context (Behave context): The Behave context object.
        string_with_placeholders (str): The string with placeholders to be replaced.

    Returns:
        str: The string with placeholders replaced by values from the context.
    Replace placeholders in the table with actual context variable values using string.Template.
    """
    pattern = r"\$(\w+)"
    matches = re.findall(pattern, string_with_placeholders)

    context_variables = {}
    for match in matches:
        context_variables[match] = getattr(context, match)

    template = string.Template(string_with_placeholders)
    return template.safe_substitute(context_variables)


@when("I wait '{seconds}' seconds")
def wait(context, seconds):
    sleep(int(seconds))


def check_value(resource: dict, field: str, value: str, type: str):
    """
    Check the value of a field in a resource against a given value and type.

    Parameters:
        resource (dict): The resource containing the field to be checked.
        field (str): The name of the field to be checked.
        value (str): The value to compare against the field value.
        type (str): The type of the field value.

    Returns:
        bool: True if the field value matches the given value and type, False otherwise.
    """
    if value == "NULL":
        return resource.get(field) is None
    elif value == "NOT_NULL":
        return resource.get(field) is not None
    elif value == "EMPTY":
        return not bool(resource.get(field))
    elif type == "integer":
        return resource.get(field) == int(value)
    elif type == "float":
        return resource.get(field) == float(value)
    elif type == "boolean":
        return resource.get(field) == bool(value)
    elif type in ["array", "object"]:
        return str(resource.get(field)) == value
    else:
        return str(resource.get(field)) == value
