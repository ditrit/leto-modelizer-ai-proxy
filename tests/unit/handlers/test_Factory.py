import pytest
from unittest.mock import MagicMock

from src.configuration.configurationManager import ConfigurationManager
from src.handlers.Factory import Factory
from src.handlers.Ollama.OllamaHandler import OllamaHandler
from src.handlers.Gemini.GeminiHandler import GeminiHandler


def test_get_all_handlers():
    all_handlers = Factory.get_all_handlers()
    assert type(all_handlers) == dict
    assert type(all_handlers["ollama"]) == OllamaHandler
    assert type(all_handlers["gemini"]) == GeminiHandler


@pytest.mark.parametrize(
    "plugin_name, configuration, expected_ai",
    [
        (
            "default",
            {
                "plugin": {"preferences": {"default": "ollama"}},
                "ollama": {
                    "base_url": "http://localhost:11434/api",
                    "models": ["mistral"],
                    "defaultModel": "mistral",
                    "modelFiles": {
                        "generate": {
                            "default": 'FROM mistral SYSTEM """ test generate """'
                        },
                        "message": {
                            "default": 'FROM mistral SYSTEM """ test message """'
                        },
                    },
                },
            },
            OllamaHandler,
        ),
        (
            "default",
            {
                "plugin": {"preferences": {"default": "gemini"}},
                "gemini": {
                    "base_url": "http://localhost:11434/api",
                    "key": "key",
                    "system_instruction": {
                        "generate": {
                            "default": '{"system_instruction":{"parts":{"text": "test"}}}'
                        },
                        "message": {
                            "default": '{"system_instruction":{"parts":{"text": "test2"}}}'
                        },
                    },
                },
            },
            GeminiHandler,
        ),
    ],
)
def test_get_handler(plugin_name, configuration, expected_ai):

    # Mock the get_configuration function
    config_manager1 = ConfigurationManager()
    config_manager1.get_configuration = MagicMock()
    config_manager1.get_configuration.return_value = configuration

    # Mock the get_all_handlers function in order to avoir calling initialize_configuration
    mocked_ollama_handler = OllamaHandler()
    mocked_ollama_handler.initialize_configuration = MagicMock()
    mocked_gemini_handler = GeminiHandler()
    mocked_gemini_handler.initialize_configuration = MagicMock()
    Factory.get_all_handlers = MagicMock()
    Factory.get_all_handlers.return_value = {
        "ollama": mocked_ollama_handler,
        "gemini": mocked_gemini_handler,
    }

    assert type(Factory.get_handler(plugin_name)) == expected_ai


def test_intialize_models_with_given_handlers():

    mocked_handler = MagicMock()
    mocked_handler.initialize_configuration = MagicMock()
    mocked_handler.initialize.return_value = "response1"

    mocked_handler2 = MagicMock()
    mocked_handler2.initialize_configuration = MagicMock()
    mocked_handler2.initialize.return_value = "response2"

    Factory.get_handler = MagicMock()
    Factory.get_handler.side_effect = [mocked_handler, mocked_handler2]
    res = Factory.initialize_models(["fake_handler", "fake_handler2"])
    assert mocked_handler.initialize.call_count == 1
    assert mocked_handler2.initialize.call_count == 1
    assert res == ["response1", "response2"]


def test_intialize_all_models():

    # Mock the get_all_handlers function in order to avoir calling initialize_configuration
    mocked_ollama_handler = OllamaHandler()
    mocked_ollama_handler.initialize_configuration = MagicMock()
    mocked_ollama_handler.initialize = MagicMock()
    mocked_ollama_handler.initialize.return_value = "response1"
    mocked_gemini_handler = GeminiHandler()
    mocked_gemini_handler.initialize_configuration = MagicMock()
    mocked_gemini_handler.initialize = MagicMock()
    mocked_gemini_handler.initialize.return_value = "response2"
    Factory.get_all_handlers = MagicMock()
    Factory.get_all_handlers.return_value = {
        "ollama": mocked_ollama_handler,
        "gemini": mocked_gemini_handler,
    }

    res = Factory.initialize_models()
    assert res == ["response1", "response2"]


def test_get_all_configuration_descriptions():
    descriptions = Factory.get_all_configuration_descriptions()

    assert "ollama" in descriptions
    assert descriptions["ollama"][0]["key"] == "base_url"
    assert descriptions["ollama"][1]["defaultValue"] == "mistral"
    assert descriptions["ollama"][2]["key"] == "allowRawResults"
    assert descriptions["ollama"][3]["type"] == "textarea"

    assert "gemini" in descriptions
    assert descriptions["gemini"][0]["key"] == "base_url"
    assert descriptions["gemini"][1]["defaultValue"] == ""
    assert descriptions["gemini"][2]["key"] == "system_instruction.generate.default"
    assert descriptions["gemini"][3]["type"] == "textarea"
