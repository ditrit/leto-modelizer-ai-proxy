import pytest
from unittest.mock import patch

from src.handlers.Factory import Factory
from src.handlers.OllamaHandler import OllamaHandler


@pytest.mark.parametrize(
    "plugin_name, configuration, expected_ai",
    [
        ("default", {"pluginPreferences": {"default": "ollama"}}, OllamaHandler),
    ],
)
def test_get_handlers(plugin_name, configuration, expected_ai):

    with patch(
        "src.configuration.configurationManager.ConfigurationManager.get_configuration"
    ) as mock_get_configuration:
        mock_get_configuration.return_value = configuration

        assert type(Factory.get_handler(plugin_name)) == expected_ai
