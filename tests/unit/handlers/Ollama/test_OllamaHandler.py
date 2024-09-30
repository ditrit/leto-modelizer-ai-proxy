import json
import requests
import pytest
from unittest.mock import patch
from unittest import TestCase

from fastapi.exceptions import HTTPException

from src.handlers.Ollama.OllamaHandler import OllamaHandler
from src.models.Diagram import Diagram
from src.models.Message import Message


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
                            "generate": {
                                "default": "default-mistral-modelfile_generate",
                                "@ditrit/kubernator-plugin": "default-kubernetes-mistral-modelfile_generate",
                                "@ditrit/githubator-plugin": "default-githubactions-mistral-modelfile_generate",
                            },
                            "message": {
                                "default": "default-mistral-modelfile_message",
                                "@ditrit/kubernator-plugin": "default-kubernetes-mistral-modelfile_message",
                                "@ditrit/githubator-plugin": "default-githubactions-mistral-modelfile_message",
                            },
                        },
                    }
                },
            }

            self.handler = OllamaHandler()

    def test_initialize(self):

        with patch("builtins.open") as mock_open:
            mock_modelfiles_content = [
                "modelfile1",
                "modelfile2",
                "modelfile3",
                "modelfile4",
                "modelfile5",
                "modelfile6",
            ]
            mock_open.return_value.__enter__.return_value.read.side_effect = (
                mock_modelfiles_content
            )
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
                    {"response": "success"},
                    {"response": "success"},
                    {"response": "success"},
                ]

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

    def test_send_message_with_files_and_context(self):
        """
        Test if files, context, and message are given, it returns a context and a message.
        And 2 calls are made, 1 for giving files and the other for the actual question.
        """
        message = Message(
            pluginName="@ditrit/githubator-plugin",
            message="Generate code",
            files=[
                {
                    "path": "path/to/file",
                    "content": "content of the file",
                }
            ],
            context="[123,456,789]",
        )

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            response1 = requests.Response()
            response1.status_code = 200
            response1._content = b'{"response": "success", "context": [1,2,3]}'
            response1.encoding = "utf-8"

            response2 = requests.Response()
            response2.status_code = 200
            response2._content = b'{"response": "success2", "context": [4,5,6]}'
            response2.encoding = "utf-8"

            mock_post.side_effect = [response1, response2]

            response_final = self.handler.send_message(message)

            response_final = json.loads(response_final.body.decode("utf-8"))

            assert mock_post.call_count == 2
            assert response_final["message"] == "success2"
            assert response_final["context"] == "[4, 5, 6]"

    def test_send_message_without_files_and_context(self):
        """Test if no files and no context are given, it returns a context and a message."""
        message = Message(
            pluginName="@ditrit/githubator-plugin",
            message="Generate code",
        )

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            response1 = requests.Response()
            response1.status_code = 200
            response1._content = b'{"response": "success", "context": [1,2,3]}'
            response1.encoding = "utf-8"

            mock_post.side_effect = [response1]

            response_final = self.handler.send_message(message)

            response_final = json.loads(response_final.body.decode("utf-8"))

            assert mock_post.call_count == 1
            assert response_final["message"] == "success"
            assert response_final["context"] == "[1, 2, 3]"

    def test_send_message_without_message_and_context(self):
        """
        Test if the message is empty, it should return only a context.
        Because its only providing files in order to ask questions about the files on a next call.
        """
        message = Message(
            pluginName="@ditrit/githubator-plugin",
            files=[
                {
                    "path": "path/to/file",
                    "content": "content of the file",
                }
            ],
        )

        with patch("src.handlers.Ollama.OllamaHandler.requests.post") as mock_post:
            response1 = requests.Response()
            response1.status_code = 200
            response1._content = b'{"response": "success", "context": [1,2,3]}'
            response1.encoding = "utf-8"

            mock_post.side_effect = [response1]

            response_final = self.handler.send_message(message)

            response_final = json.loads(response_final.body.decode("utf-8"))

            assert mock_post.call_count == 1
            assert "message" not in response_final
            assert response_final["context"] == "[1, 2, 3]"
