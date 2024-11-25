from src.configuration.configurationManager import ConfigurationManager
from src.handlers.Ollama.OllamaHandler import OllamaHandler
from src.handlers.Gemini.GeminiHandler import GeminiHandler


class Factory:
    """
    Factory class for handling adequate handler objects.
    """

    @staticmethod
    def get_all_handlers():
        """
        Retrieves all the names of the handlers that are available.

        Returns:
            dict: A dictionary with the handler names as keys and the handler objects as values.
        """
        return {"ollama": OllamaHandler(), "gemini": GeminiHandler()}

    @staticmethod
    def get_handler(plugin_name: str):
        """
        Retrieves a handler object based on the specified plugin name.

        Parameters:
            plugin_name (str): The name of the plugin for which the handler is needed.

        Returns:
            OllamaHandler: The handler object for the specified plugin name, or None if the plugin name is not found or the configuration value is not "ollama".
        """

        configuration_manager = ConfigurationManager()

        # Retrieve the configuration after ensuring it is set
        configuration = configuration_manager.get_configuration()

        handler_name = (
            configuration.get("plugin", {}).get("preferences", {}).get(plugin_name)
            or configuration.get("plugin", {}).get("preferences", {}).get("default")
            or "ollama"
        )
        handler = Factory.get_all_handlers().get(handler_name)
        handler.initialize_configuration()

        return handler

    @staticmethod
    def initialize_models(handlers: set[str] | None = None):
        """
        Initializes all the models defined in the configuration file.

        Parameters:
            handlers (set[str] | None, optional): The handler names to initialize. Defaults to None.
        """
        responses = []
        if handlers:
            for handler in handlers:
                handler_instance = Factory.get_handler(handler)
                if handler_instance:
                    handler_instance.initialize_configuration()
                    responses.append(handler_instance.initialize())
        else:
            for handler_instance in Factory.get_all_handlers().values():
                handler_instance.initialize_configuration()
                responses.append(handler_instance.initialize())
        return responses

    @staticmethod
    def get_all_configuration_descriptions():
        """
        Retrieves all the descriptions of the configuration fields used by all the handlers.

        Returns:
            dict: A dictionary with the handler names as keys and the descriptions as values.
        """
        configuration_description = {}
        for ai_name, handler in Factory.get_all_handlers().items():
            description = handler.get_configuration_description()
            configuration_description[ai_name] = description

        return configuration_description
