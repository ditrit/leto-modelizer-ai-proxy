from src.configuration.configurationManager import ConfigurationManager
from src.handlers.OllamaHandler import OllamaHandler


class Factory:
    """
    Factory class for creating adequate handler objects.
    """

    @staticmethod
    def get_handler(plugin_name: str):
        """
        Retrieves a handler object based on the specified plugin name.

        Parameters:
            plugin_name (str): The name of the plugin for which the handler is needed.

        Returns:
            OllamaHandler: The handler object for the specified plugin name, or None if the plugin name is not found or the configuration value is not "ollama".
        """
        configuration = ConfigurationManager().get_configuration()

        plugin_name = configuration["pluginPreferences"].get(
            plugin_name
        ) or configuration["pluginPreferences"].get("default")

        if plugin_name == "ollama":
            return OllamaHandler()
