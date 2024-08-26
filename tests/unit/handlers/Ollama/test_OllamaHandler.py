import json
import requests
import pytest
from unittest.mock import patch
from unittest import TestCase

from fastapi.exceptions import HTTPException

from src.handlers.Ollama.OllamaHandler import OllamaHandler
from src.models.Diagram import Diagram


class TestOllamaHandler(TestCase):

    def setUp(self) -> None:
        with patch(
            "src.handlers.BaseHandler.ConfigurationManager.get_configuration"
        ) as mock_get_configuration:

            mock_get_configuration.return_value = {
                "pluginPreferences": {"default": "ollama"},
                "ai-models": {
                    "ollama": {
                        "base_url": "http://localhost",
                        "models": ["mistral"],
                        "defaultModel": "mistral",
                        "modelFiles": {
                            "default": "default-mistral-modelfile",
                            "kubernator-plugin": "default-kubernetes-mistral-modelfile",
                            "githubator-plugin": "default-githubactions-mistral-modelfile",
                        },
                    }
                },
            }

            self.handler = OllamaHandler()

    def test_generate(self):
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value._content = (
                b'{"response": "```json {\\"random\\": 5}```"}'
            )
            mock_post.return_value.encoding = "utf-8"

            response = self.handler.generate(diagram)
            assert json.loads(response.body.decode("utf-8")) == {"random": 5}

    def test_generate_not_correct_format(self):
        """
        Test if the response is not in the correct format.
        I.E, the returned code is not in a code block.
        """
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value._content = b'{"response": "{\\"random\\": 5}"}'
            mock_post.return_value.encoding = "utf-8"

            with pytest.raises(HTTPException, match="Invalid response from Ollama API"):
                self.handler.generate(diagram)

    def test_generate_not_json(self):
        """
        Test if the response is not in the correct format.
        I.E, the returned code is not a json.
        """
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value._content = b'{"response": "random"}'
            mock_post.return_value.encoding = "utf-8"

            with pytest.raises(HTTPException, match="Invalid response from Ollama API"):
                self.handler.generate(diagram)

    def test_initialize(self):

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value._content = b'{"response": "success"}'
            mock_post.return_value.encoding = "utf-8"

            responses = self.handler.initialize()
            assert responses == [
                {"response": "success"},
                {"response": "success"},
                {"response": "success"},
            ]
