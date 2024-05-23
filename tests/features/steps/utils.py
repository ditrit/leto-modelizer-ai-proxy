import json
import string


def table_to_json(context):
    """
    Convert Behave context table to JSON format

    The table should have the following structure:
    | key  | value  | type    |
    | key1 | value1 | string  |
    | key2 | value2 | string  |
    | key3 | 2      | integer |

    The JSON format will be:
    {
        "key1": "value1",
        "key2": "value2",
        "key2": 2
    }

    The type parameter is used to specify the type of the value in the table,
    and the type should be a type, such as string, integer, float, list, json etc.
    By default the type (if not specified) is string.

    Parameters:
        context (Behave context): The context object.

    Returns:
        dict: A dictionary containing the table data.
    """
    data = {}
    for row in context.table:
        key, value, json_type = row["key"], row["value"], row["type"]
        value = replace_values_in_string(context, value)
        print(f"value: {value}, type: {type(value)}")
        if not json_type:
            data[key] = value
        elif json_type == "integer":
            data[key] = int(value)
        elif json_type == "float":
            data[key] = float(value)
        elif json_type == "boolean":
            data[key] = bool(value)
        elif json_type == "json":
            data[key] = json.loads(value)
        else:
            data[key] = value

    return data


def replace_values_in_string(context, string_with_placeholders: str):
    """
    Replaces values in a string with values from the Behave context.

    Parameters:
        context (Behave context): The Behave context object.
        string_with_placeholders (str): The string with placeholders to be replaced.

    Returns:
        str: The string with placeholders replaced by values from the context.
    """
    template = string.Template(string_with_placeholders)
    return template.substitute(context)


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
