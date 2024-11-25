import os
import json
import inspect
from abc import ABC, abstractmethod

from src.configuration.configurationManager import ConfigurationManager
from src.models.Diagram import Diagram
from src.models.Message import Message


class BaseHandler(ABC):
    """
    Base class for all handler classes.
    """

    def __init__(self, ai_name: str):
        """
        Initializes the BaseHandler by setting the `configuration` from the user configuration.

        Parameters:
            ai_name (str): The name of the AI model to use for the handler.
        """
        self.ai_name = ai_name
        self.configuration = None

    def initialize_configuration(self):
        self.configuration = ConfigurationManager().get_configuration()[self.ai_name]

    @abstractmethod
    def initialize(self):
        """
        This method is used to initialize everything the handler needs in order to work.
        """
        pass

    @abstractmethod
    def generate(self, diagram: Diagram):
        """
        Generates code based on the provided `diagram` object.

        Parameters:
            diagram (Diagram): The diagram object containing the description of the diagram to generate.
        """
        pass

    @abstractmethod
    def send_message(self, message: Message):
        """
        Sends a message to the AI.
        The message is a message in a conversation.

        Parameters:
            message (Message): The message object containing the message to send to the AI.
        """
        pass

    def get_configuration_description(self, file_name: str = None):
        """
        Returns the description of the configuration fields that are used by the handler.

        Parameters:
            file_name (str, optional): The name of the file to get the description of.
            If None, the description of the default file is used (description.json).

        Returns:
            str: The description of the file.
        """
        # Get the directory of the current class (child class)        # Get the file path of the child class
        child_class_file = inspect.getfile(self.__class__)

        # Get the directory where the child class file is located
        child_class_dir = os.path.dirname(os.path.abspath(child_class_file))

        file_name = file_name or "configuration_description.json"
        json_file_path = os.path.join(child_class_dir, file_name)
        # Read the JSON file and return its contents
        try:
            with open(json_file_path, "r") as file:
                description = json.load(file)
            return description
        except FileNotFoundError:
            return "JSON file not found in the class's folder."
