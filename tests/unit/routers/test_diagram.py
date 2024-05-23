import pytest
import requests_mock
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "plugin_name, description, expected_response",
    [
        (
            "default",
            "what is the meaning of life",
            {
                "model": "mistral",
                "created_at": "2024-05-16T12:33:40.779040316Z",
                "response": "The meaning of life is 42.",
            },
        ),
    ],
)
def test_generate_diagram(plugin_name, description, expected_response, client):

    with patch("src.routers.diagram.Factory.get_handler") as mock_get_handler:
        mock_get_handler.return_value.generate.return_value = expected_response

        body = {"pluginName": plugin_name, "description": description}
        response = client.post("/api/diagram/", json=body)
        assert response.status_code == 200
        assert response.json() == expected_response


def test_404(client):
    """
    A test function for handling a 404 response status code.
    It sends a GET request to a non-existent endpoint "/nope/oupsie" and checks if the response status code is 404.
    """

    response = client.get("/nope/oupsie")
    assert response.status_code == 404
