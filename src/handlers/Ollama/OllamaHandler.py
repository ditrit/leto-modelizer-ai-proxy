import os
import requests
import json
import re

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
            for model_file in self.configuration["modelFiles"]:
                print(f"Loading Ollama model file: {model_file}")
                body = {
                    "name": model_file,
                    "path": os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "ModelFiles",
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
            r"```json\s*([^`]+)```",  # NOSONAR: Sonar do not want the + in the regexp, but it is required
            response_text,
            re.DOTALL,
        )
        if json_match:
            json_data = json_match.group(1)
            try:
                json.loads(json_data)
                return json_data
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
        else:
            model = self.configuration["modelFiles"][0]
        print(f"Generating code with Ollama model: {model}")
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

        if json_code is None:
            return response.json()["response"]
        else:
            return json_code
