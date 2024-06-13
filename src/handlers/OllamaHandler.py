import requests

from src.models.Diagram import Diagram
from src.handlers.BaseHandler import BaseHandler


class OllamaHandler(BaseHandler):

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
        body = {
            "model": self.configuration["ollama"]["defaultModel"],
            "prompt": diagram.description,
            "stream": False,
        }

        response = requests.post(
            f"{self.configuration['ollama']['base_url']}/generate", json=body
        )

        return response.json()["response"]
