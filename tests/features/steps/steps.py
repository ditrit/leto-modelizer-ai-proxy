import os
import requests
from behave import when, then

from utils import table_to_json, replace_values_in_string, check_value


@when('I request "{endpoint}" with method "{method}" with json')
def step_when_send_request_with_json(context, endpoint, method):
    if context.table:
        context.request_data = table_to_json(context)
    request_full(context, endpoint, method, context.request_data, "application/json")


@when('I request "{endpoint}" with method "{method}"')
def step_when_send_request(context, endpoint, method):
    request_full(context, endpoint, method, None, None)


def request_full(context, endpoint: str, method: str, body: dict, content_type: str):
    if endpoint == "/":
        endpoint = ""
    endpoint = replace_values_in_string(context, endpoint)
    context.url = os.path.join("http://localhost:8585", endpoint)

    header = {}
    if content_type:
        header["Content-Type"] = content_type

    if getattr(context, "csrf_header", None):
        header[context.csrf_header] = context.csrf_header

    print(f"{method} request with uri: {context.url}")
    if body:
        print(f"Request with body: {body}")
    else:
        print("Request without body")

    context.response = requests.request(method, context.url, json=body, headers=header)

    print(f"Request status code: {context.response.status_code}")
    print(f"Response body: {context.response.text}")


@then("I expect {status_code} as status code")
def step_then_check_status_code(context, status_code):
    assert context.response.status_code == int(
        status_code
    ), f"Expected status code {status_code}, but got {context.response.status_code}"


@then('I expect object field "{field}" is "{content}"')
def step_then_check_status_code(context, field, content):
    value = replace_values_in_string(context, content)

    assert check_value(context.response.json(), field, value, "string")


@then('I save the field "{field}" of the response in the context')
def step_save_field_in_context(context, field):
    json_data = context.response.json()
    keys = field.split(".")

    # Traverse through the keys to access the nested value
    for key in keys:
        json_data = json_data[key]

    # Save the final value in the context using the last part of the key
    setattr(context, keys[-1], json_data)
