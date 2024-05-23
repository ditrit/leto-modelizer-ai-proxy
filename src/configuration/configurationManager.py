import os
import json


class ConfigurationManager:
    """
    A Singleton class for managing configuration settings.
    """

    _instance = None
    _reset = False

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class.

        This method is a special method in Python that is called when a new instance of the class is created.
        It is responsible for creating and returning a new instance of the class.

        Parameters:
            cls (type): The class object.
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.

        Returns:
            object: The newly created instance of the class.

        Note:
            This method is used to implement the Singleton design pattern, where only one instance of the class can exist.
            It ensures that only one instance of the class is created and returned whenever a new instance is requested.
        """

        if not cls._instance or cls._reset:
            cls._instance = super().__new__(cls)
            cls._reset = False
        return cls._instance

    def reset(cls):
        """
        Resets the class by setting the `_instance` attribute to `None` and the `_reset` attribute to `True`.

        Parameters:
            cls (type): The class object.
        """
        cls._instance = None
        cls._reset = True

    def __validate_configuration(self, configuration):
        """
        Validates the given configuration by checking if the AI models specified in the plugin preferences are valid.

        Parameters:
            configuration (dict): The configuration to be validated.

        Raises:
            ValueError: If an invalid AI model is found in the plugin preferences.

        Returns:
            dict: The validated configuration.
        """
        if not "default" in configuration["pluginPreferences"]:
            raise ValueError("Invalid plugin preferences: 'default' not found")
        for _, ai_to_use in configuration["pluginPreferences"].items():
            if ai_to_use not in configuration:
                raise ValueError(f"Invalid AI: { ai_to_use }")
        return configuration

    def get_configuration(self):
        """
        Retrieves the configuration settings from a JSON file.

        This method checks if the configuration has already been loaded.
        If not, it reads the configuration settings from a JSON file located at the path specified by the environment variable `API_CONFIGURATION`.
        If the environment variable is not set, it defaults to `src/configuration/configuration.json`.
        The method opens the file, parses its contents as JSON, and stores the configuration settings in the `_config` attribute.

        Returns:
            dict: The configuration settings as a dictionary.

        Raises:
            FileNotFoundError: If the configuration file specified by `API_CONFIGURATION` does not exist.
            JSONDecodeError: If the configuration file contains invalid JSON syntax.
        """
        if not hasattr(self, "_config"):
            config_file_path = os.environ.get(
                "API_CONFIGURATION", "src/configuration/configuration.json"
            )
            with open(config_file_path, "r") as configuration_file:
                self._config = self.__validate_configuration(
                    json.load(configuration_file)
                )
        return self._config
