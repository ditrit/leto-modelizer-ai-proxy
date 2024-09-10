from pydantic import BaseModel, Field
from typing import List, Optional


class FileModel(BaseModel):
    """
    A Pydantic model that defines the structure of a file object.

    This class is used to send a file to the AI during a conversation.
    The conversation is handled by Leto-Modelizer-Api itself.

    The path is the path of the file to send to the AI.
    The content is the content of the file to send to the AI.
    """

    path: str
    content: str


class Message(BaseModel):
    """
    A Pydantic model that defines the structure of a message object.

    This class is used to send a message to the AI during a conversation.
    The conversation is handled by Leto-Modelizer-Api itself.

    The plugin_name is the name of the plugin used to generate the diagram.
    The message is the message to send to the AI.
    The context is the context of the message to send to the AI.
    The files is a list of files to send to the AI for the context.
    """

    plugin_name: str = Field(validation_alias="pluginName")
    files: Optional[List[FileModel]] = None
    message: Optional[str] = None
    context: Optional[str] = None
