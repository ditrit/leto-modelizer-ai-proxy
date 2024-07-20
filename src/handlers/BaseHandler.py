from abc import ABC, abstractmethod

from src.configuration.configurationManager import ConfigurationManager
from src.models.Diagram import Diagram


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
        self.configuration = ConfigurationManager().get_configuration()["ai-models"][
            ai_name
        ]

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
