from abc import ABC, abstractmethod

from src.configuration.configurationManager import ConfigurationManager
from src.models.Diagram import Diagram


class BaseHandler(ABC):
    """
    Base class for all handler classes.
    """

    def __init__(self):
        """
        Initializes the BaseHandler by setting the `configuration` from the user configuration.
        """
        self.configuration = ConfigurationManager().get_configuration()

    @abstractmethod
    def generate(self, diagram: Diagram):
        """
        Generates code based on the provided `diagram` object.

        Parameters:
            diagram (Diagram): The diagram object containing the description of the diagram to generate.
        """
        pass
