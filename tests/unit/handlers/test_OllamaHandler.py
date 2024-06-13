import requests
from unittest.mock import patch
from unittest import TestCase

from src.handlers.OllamaHandler import OllamaHandler
from src.models.Diagram import Diagram


class TestOllamaHandler(TestCase):

    def setUp(self) -> None:
        with patch(
            "src.handlers.BaseHandler.ConfigurationManager.get_configuration"
        ) as mock_get_configuration:

            mock_get_configuration.return_value = {
                "pluginPreferences": {"default": "ollama"},
                "ollama": {
                    "base_url": "http://localhost:11434/api",
                    "models": ["mistral"],
                    "defaultModel": "mistral",
                },
            }

            self.handler = OllamaHandler()

    def test_generate(self):
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.OllamaHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mock_post.return_value._content = b'{"response": "Hello you"}'
            mock_post.return_value.encoding = "utf-8"

            response = self.handler.generate(diagram)
            assert response == "Hello you"
