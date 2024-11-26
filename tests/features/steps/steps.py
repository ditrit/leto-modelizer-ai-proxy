import os
import requests
from behave import when, then

from utils import (
    table_to_json,
    basic_table_to_dict,
    replace_values_in_string,
    check_value,
    encrypt_test_function,
)


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

    headers = {}
    if content_type:
        headers["Content-Type"] = content_type

    if getattr(context, "csrf_header", None):
        headers[context.csrf_header] = context.csrf_header

    print(f"{method} request with uri: {context.url}")
    if body:
        print(f"Request with body: {body}")
    else:
        print("Request without body")

    if headers.get("Content-Type") == "application/json":
        context.response = requests.request(
            method, context.url, json=body, headers=headers
        )
    else:
        context.response = requests.request(
            method, context.url, data=body, headers=headers
        )

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


@then('I expect the response field "{field_name}" to be "{value}"')
def check_field_to_be_value(context, field_name, value):
    """
    field_name: The name of the field to check (supports dot notation and array indices like "field1.field2[0].field3")
    value: The expected value of the field
    """
    # Split the field_name by dots, but keep array indices intact
    fields = field_name.split(".")
    current = context.response.json()

    for field in fields:
        # Check if it's an array index like 'field[0]'
        if "[" in field and "]" in field:
            # Extract field name and index
            base_field = field[: field.index("[")]
            index = int(field[field.index("[") + 1 : field.index("]")])

            # Navigate to the array
            if base_field in current and isinstance(current[base_field], list):
                current = current[base_field][index]
            else:
                current = None
                break
        else:
            # Normal field navigation
            if field in current:
                current = current[field]
            else:
                current = None
                break

    # Assert that the field value matches the expected value
    actual_value = current
    assert str(actual_value) == str(
        value
    ), f"Expected {field_name} = {value}, but got {actual_value if actual_value else 'None'}"


@when(
    "I encrypt the configuration with secret decryption key (from env) and save it in the context"
)
def step_encrypt_config(context):
    config_json = basic_table_to_dict(context)
    key = os.getenv("DECRYPTION_KEY")
    context.encrypted_config = encrypt_test_function(key, config_json)


@when('I request "{endpoint}" with method "{method}" with encrypted configuration')
def step_when_send_request_with_json(context, endpoint, method):
    request_full(
        context, endpoint, method, context.encrypted_config, "application/octet-stream"
    )


@when("I set Ollama modelFiles in the context")
def step_set_ollama_model_files(context):
    default_generate = """
                        FROM mistral
                        SYSTEM \"\"\"
                        You are an experienced Devops engineer:

                        For any other topics the response must be: 'I am not programmed to answer that.'

                        When given specifications for a particular need or application you know the best way to create it.
                        The response must be an array, in which, each item must be a json. Each json must have 2 fields that are 'name' and 'content', with the name being the name of the file and the content being the generated code.
                        Moreover, it is absolutely necessary that the array is wrapped in a json code block with openning and closing, such as:

                        \[
                        [
                            {
                                "name": "deploy.yaml",
                                "content": "apiVersion: apps/v1\\nkind: Deployment\\nmetadata:\\n  name: my-deployment\\nspec:\\n  selector:\\n    matchLabels:\\n      app: my-app\\n  replicas: 1\\n  template:\\n    metadata:\\n      labels:\\n        app: my-app\\n    spec:\\n      containers:\\n      - name: my-container\\n        image: nginx"
                            }
                        ]
                        \"\"\"
                        """
    default_message = """
                      FROM mistral
                      SYSTEM \"\"\"
                      You are an experienced Devops engineer focused on the following subjects:
                      - Kubernetes
                      - Terraform
                      - Github Actions
                      - Docker
                      
                      For any other topics the response must be: 'I am not programmed to answer that.'
                      
                      When given specifications for a particular need or application you know the best way to create it.
                      Format your response using HTML markup to make it more presentable and for each line a maximum length of 100 characters.
                      Here is an exemple of a response: \"<strong> In order to create a container </strong>\"
                      \"\"\"
                      """
    context.default_generate = default_generate
    context.default_message = default_message
