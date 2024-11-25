import json
import requests
import pytest
from unittest.mock import patch
from unittest import TestCase

from fastapi.exceptions import HTTPException

from src.handlers.Gemini.GeminiHandler import GeminiHandler
from src.models.Diagram import Diagram
from src.models.Message import Message


class TestGeminiHandler(TestCase):

    def setUp(self) -> None:
        with patch(
            "src.handlers.BaseHandler.ConfigurationManager.get_configuration"
        ) as mock_get_configuration:

            mock_get_configuration.return_value = {
                "gemini": {
                    "base_url": "https://localhost",
                    "key": "coucou",
                    "system_instruction": {
                        "generate": {
                            "default": '{"system_instruction":{"parts":{"text": "test"}}}'
                        },
                        "message": {
                            "default": '{"system_instruction":{"parts":{"text": "test2"}}}'
                        },
                    },
                }
            }

            self.handler = GeminiHandler()
            self.handler.initialize_configuration()

    def test_initialize(self):
        """
        Since the initialiaze return always true, nothing more to test.
        """
        assert self.handler.initialize()

    def test_generate(self):
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.Gemini.GeminiHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mocked_response = b'{"candidates": [{"content": {"parts": [{"text": "{\\"random\\": 5}"}]}}]}'
            mock_post.return_value._content = mocked_response
            mock_post.return_value.encoding = "utf-8"

            response = self.handler.generate(diagram)
            assert json.loads(response.body.decode("utf-8")) == {"random": 5}

    def test_generate_not_json(self):
        """
        Test if the response is not in the correct format.
        I.E, the returned code is not a json formatted.
        """
        diagram = Diagram(pluginName="default", description="Generate code")

        with patch("src.handlers.Gemini.GeminiHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mocked_response = (
                b'{"candidates": [{"content": {"parts": [{"text": "coucou"}]}}]}'
            )
            mock_post.return_value._content = mocked_response
            mock_post.return_value.encoding = "utf-8"

            with pytest.raises(HTTPException, match="Invalid response from Gemini API"):
                self.handler.generate(diagram)

    def test_send_message_with_files(self):
        """
        Test if files are given, it returns a response with a "no context" context.
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
        )

        response_final = self.handler.send_message(message)
        response_final = json.loads(response_final.body.decode("utf-8"))
        assert response_final["context"] == "no context"

    def test_send_message_without_files(self):
        """Test if no files are given, it returns a context ("no context") and a message."""
        message = Message(
            pluginName="@ditrit/githubator-plugin",
            message="Generate code",
        )

        with patch("src.handlers.Gemini.GeminiHandler.requests.post") as mock_post:
            mock_post.return_value = requests.Response()
            mock_post.return_value.status_code = 200
            mocked_response = (
                b'{"candidates": [{"content": {"parts": [{"text": "hey you !"}]}}]}'
            )
            mock_post.return_value._content = mocked_response
            mock_post.return_value.encoding = "utf-8"

            response_final = self.handler.send_message(message)
            response_final = json.loads(response_final.body.decode("utf-8"))

            assert mock_post.call_count == 1
            assert response_final["message"] == "hey you !"
            assert response_final["context"] == "no context"

    def test_send_message_without_message_and_context(self):
        """
        Test if the message is empty, it should return only a context ("no context").
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

        response_final = self.handler.send_message(message)
        response_final = json.loads(response_final.body.decode("utf-8"))
        assert response_final["context"] == "no context"
