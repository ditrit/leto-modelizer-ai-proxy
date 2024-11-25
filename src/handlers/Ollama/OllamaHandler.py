import requests
import json
import re

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.models.Message import Message
from src.models.Diagram import Diagram
from src.handlers.BaseHandler import BaseHandler


class OllamaHandler(BaseHandler):
    """
    Ollama handler class.

    This class is used to generate code using the Ollama API.

    The handler must be initialized with the `configuration` from the user configuration, using the `initialize_configuration` method.
    """

    def __init__(self):
        """
        Initializes the OllamaHandler by setting the `configuration` from the user configuration.
        """
        super().__init__("ollama")

    def initialize(self):
        """
        This method is used to initialize everything the handler needs in order to work.

        For Ollama, this method will load all the ModelFiles defined in the configuration file.
        """

        reponses = []
        if "modelFiles" in self.configuration:
            for model_file_category, model_files in self.configuration[
                "modelFiles"
            ].items():
                for plugin_name, model_file_content in model_files.items():
                    print(
                        f"Loading Ollama model file for {plugin_name} ({model_file_category})"
                    )

                    body = {
                        "name": f"{plugin_name}_{model_file_category}",
                        "modelfile": model_file_content,
                        "stream": False,
                    }

                    response = requests.post(
                        f"{self.configuration['base_url']}/create",
                        json=body,
                    )

                    reponses.append(response.json())

        return reponses

    def __parse_response(self, response_text):
        """
        Parse the response text to extract JSON data.

        Parameters:
            response_text (str): The text containing the JSON data.

        Returns:
            str: The extracted JSON data if successfully parsed, otherwise None.
        """
        allow_raw_results = (
            True if self.configuration.get("allowRawResults") == "true" else False
        )

        json_match = re.search(
            r"```(?:\w+)?\s*([\s\S]+?)```",  # NOSONAR: Sonar do not want the + in the regexp, but it is required
            response_text,
            re.DOTALL,
        )
        if json_match:
            json_data = json_match.group(1)
            try:
                return json.loads(json_data)
            except json.JSONDecodeError:
                return json_match if allow_raw_results else None
        else:
            return response_text if allow_raw_results else None

    def generate(self, diagram: Diagram):
        """
        Generates code based on the provided `diagram` object.

        Parameters:
            diagram (Diagram): The diagram object containing the description of the diagram.

        Returns:
            str: The generated response from the Ollama API.

        Raises:
            KeyError: If the configuration file does not contain the required keys.
            requests.exceptions.RequestException: If there is an error while making the API request.
        """

        if "modelFiles" not in self.configuration:
            model = self.configuration["defaultModel"]
        elif diagram.plugin_name in self.configuration["modelFiles"]["generate"]:
            model = f"{diagram.plugin_name}_generate"
        else:
            model = "default_generate"

        body = {
            "model": model,
            "prompt": diagram.description,
            "stream": False,
        }

        response = requests.post(
            f"{self.configuration['base_url']}/generate",
            json=body,
        )

        json_code = self.__parse_response(response.json()["response"])
        if json_code is not None:
            return JSONResponse(content=json_code)
        else:
            raise HTTPException(
                status_code=530, detail="Invalid response from Ollama API"
            )

    def send_message(self, message: Message):

        if "modelFiles" not in self.configuration:
            model = self.configuration["defaultModel"]
        elif message.plugin_name in self.configuration["modelFiles"]["message"]:
            model = f"{message.plugin_name}_message"
        else:
            model = "default_message"

        # If there are files, add them to the prompt in order to
        # provide more context to the model
        if message.files is not None:
            body = {
                "model": model,
                "prompt": "I'm going to ask you questions about the following files (you can forget all previous files):",
                "stream": False,
            }

            for file in message.files:
                body["prompt"] = f"{body['prompt']}\n {file.path}: {file.content}"

            if message.context is not None:
                body["context"] = message.context

            response = requests.post(
                f"{self.configuration['base_url']}/generate",
                json=body,
            )

            if "context" in response.json():
                message.context = str(response.json()["context"])
            else:
                message.context = str([])

            # If no message was provided, return only the context
            if message.message is None:
                response_context = {"context": message.context}
                return JSONResponse(content=response_context)

        body = {
            "model": model,
            "prompt": message.message,
            "stream": False,
        }

        if message.context is not None:
            body["context"] = json.loads(message.context)

        response = requests.post(
            f"{self.configuration['base_url']}/generate",
            json=body,
        )

        json_code = {"message": response.json()["response"]}
        json_code["context"] = str(response.json()["context"])
        return JSONResponse(content=json_code)
