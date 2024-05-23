import json
import pytest
from unittest import TestCase
from unittest.mock import patch
from src.configuration.configurationManager import ConfigurationManager


class TestConfigurationManager(TestCase):

    def setUp(self) -> None:
        ConfigurationManager().reset()

    def test_configuration_singleton(self):
        config_manager1 = ConfigurationManager()
        config_manager2 = ConfigurationManager()
        self.assertIs(config_manager1, config_manager2)

    @patch("os.environ.get")
    @patch("builtins.open")
    def test_configuration_validation_error(self, mock_open, mock_environ_get):
        # Mock the return value of os.environ.get
        mock_environ_get.return_value = "path/to/config.json"

        # Mock the return value of open
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = json.dumps(
            {
                "pluginPreferences": {"default": "fakeAI"},
                "ollama": {"url": "http://localhost"},
            }
        )

        with pytest.raises(ValueError, match="Invalid AI: fakeAI"):
            ConfigurationManager().get_configuration()

    @patch("os.environ.get")
    @patch("builtins.open")
    def test_configuration_validation_error_no_default(
        self, mock_open, mock_environ_get
    ):
        # Mock the return value of os.environ.get
        mock_environ_get.return_value = "path/to/config.json"

        # Mock the return value of open
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = json.dumps(
            {
                "pluginPreferences": {"somePlugin": "ollama"},
                "ollama": {"url": "http://localhost"},
            }
        )

        with pytest.raises(
            ValueError, match="Invalid plugin preferences: 'default' not found"
        ):
            ConfigurationManager().get_configuration()

    @patch("os.environ.get")
    @patch("builtins.open")
    def testsd_configuration_success(self, mock_open, mock_environ_get):
        # Mock the return value of os.environ.get
        mock_environ_get.return_value = "path/to/config.json"

        # Mock the return value of open
        mock_file = mock_open.return_value.__enter__.return_value
        expected_config = json.dumps(
            {
                "pluginPreferences": {"default": "ollama"},
                "ollama": {"url": "http://localhost"},
            }
        )

        mock_file.read.return_value = expected_config

        config = ConfigurationManager().get_configuration()

        # Assert that the function returns the expected dictionary
        self.assertEqual(config, json.loads(expected_config))
        mock_environ_get.assert_called_once_with(
            "API_CONFIGURATION", "src/configuration/configuration.json"
        )
        mock_open.assert_called_once_with("path/to/config.json", "r")
        mock_file.read.assert_called_once()
