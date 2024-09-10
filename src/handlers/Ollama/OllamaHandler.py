import os
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
                for plugin_name, model_file in model_files.items():
                    print(
                        f"Loading Ollama model file for {plugin_name}: {model_file_category}/{model_file} ({model_file_category})"
                    )
                    body = {
                        "name": model_file,
                        "path": os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            "ModelFiles",
                            model_file_category,
                            model_file,
                        ),
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
                return None
        else:
            return None

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
            model = self.configuration["modelFiles"]["generate"][diagram.plugin_name]
        else:
            model = self.configuration["modelFiles"]["generate"]["default"]

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
            model = self.configuration["modelFiles"]["message"][message.plugin_name]
        else:
            model = self.configuration["modelFiles"]["message"]["default"]

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

            message.context = str(response.json()["context"])

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
