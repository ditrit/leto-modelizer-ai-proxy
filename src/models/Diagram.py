from pydantic import BaseModel, Field


class Diagram(BaseModel):
    """
    A Pydantic model that defines the structure of a diagram object.

    The plugin_name is the name of the plugin used to generate the diagram.
    The description is the description (in clear text) of the diagram.
    """

    plugin_name: str = Field(validation_alias="pluginName")
    description: str
