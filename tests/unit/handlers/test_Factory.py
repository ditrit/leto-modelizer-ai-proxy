import pytest
from unittest.mock import patch, MagicMock

from src.handlers.Factory import Factory
from src.handlers.Ollama.OllamaHandler import OllamaHandler
from src.handlers.Gemini.GeminiHandler import GeminiHandler


@pytest.mark.parametrize(
    "plugin_name, configuration, expected_ai",
    [
        (
            "default",
            {
                "pluginPreferences": {"default": "ollama"},
                "ai-models": {
                    "ollama": {
                        "base_url": "http://localhost:11434/api",
                        "models": ["mistral"],
                        "defaultModel": "mistral",
                        "modelFiles": ["default-mistral-modelfile"],
                    },
                },
            },
            OllamaHandler,
        ),
        (
            "default",
            {
                "pluginPreferences": {"default": "gemini"},
                "ai-models": {
                    "gemini": {
                        "base_url": "http://localhost:11434/api",
                        "key": "key",
                        "system_instruction": {
                            "generate": {
                                "default": "default-generate.json",
                                "@ditrit/kubernator-plugin": "default-kubernetes.json",
                                "@ditrit/githubator-plugin": "default-githubactions.json",
                            },
                            "message": {
                                "default": "default-message.json",
                                "@ditrit/kubernator-plugin": "default-kubernetes.json",
                                "@ditrit/githubator-plugin": "default-githubactions.json",
                            },
                        },
                    },
                },
            },
            GeminiHandler,
        ),
    ],
)
def test_get_handlers(plugin_name, configuration, expected_ai):

    with patch(
        "src.configuration.configurationManager.ConfigurationManager.get_configuration"
    ) as mock_get_configuration:
        mock_get_configuration.return_value = configuration

        assert type(Factory.get_handler(plugin_name)) == expected_ai


def test_intialize_models():

    fake_configuration = {
        "pluginPreferences": {"default": "fakeAI"},
        "ai-models": {
            "fakeAI": {
                "base_url": "http://localhost:11434/api",
                "models": ["mistral"],
                "defaultModel": "mistral",
                "modelFiles": ["default-mistral-modelfile"],
            },
        },
    }

    with patch(
        "src.configuration.configurationManager.ConfigurationManager.get_configuration"
    ) as mock_get_configuration:
        mock_get_configuration.return_value = fake_configuration

        mocked_handler = MagicMock()
        Factory.get_handler = MagicMock()
        Factory.get_handler.return_value = mocked_handler
        Factory.initialize_models()
        assert mocked_handler.initialize.call_count == 1
