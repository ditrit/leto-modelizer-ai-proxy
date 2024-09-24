import os
import requests
import json
import re

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.models.Message import Message
from src.models.Diagram import Diagram
from src.handlers.BaseHandler import BaseHandler


class GeminiHandler(BaseHandler):
    """
    Gemini handler class.

    This class is used to generate code using the Gemini API.

    Note: Gemini does not handle context as we want, so chats with a context is not supported.
    """

    def __init__(self):
        """
        Initializes the GeminiHandler by setting the `configuration` from the user configuration.
        """
        super().__init__("gemini")

    def initialize(self):
        """
        This method is used to initialize everything the handler needs in order to work.

        Nothing to do here.
        """
        return True

    def __send_reqest_with_system_instructions(
        self, plugin_name: str, text: str, instruction: str = "generate"
    ):
        """
        Sends a request to the Gemini API to generate code based on the provided plugin name and text.

        Parameters:
            plugin_name (str): The name of the plugin to use for code generation.
            text (str): The text to use as input for code generation.
            instruction (str, optional): The instruction type of request to send. Defaults to "generate".

        Returns:
            JSONResponse: The generated code from the Gemini API.
        """

        body = {}

        if plugin_name in self.configuration["system_instruction"][instruction]:
            instruction_file_name = self.configuration["system_instruction"][
                instruction
            ][plugin_name]
            current_path = os.path.dirname(__file__)
            path_file = os.path.join(
                current_path, "SystemInstructions", instruction, instruction_file_name
            )
            with open(path_file) as instruction_file:
                instruction_json = json.load(instruction_file)
                body.update(instruction_json)

        body["contents"] = {"parts": {"text": f"{text}"}}
        body["generationConfig"] = {"response_mime_type": "application/json"}

        query_params = {"key": self.configuration["key"]}
        response = requests.post(
            f"{self.configuration['base_url']}",
            json=body,
            params=query_params,
        )
        print(f"---------- Response: {response.json()}")
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    def generate(self, diagram: Diagram):
        """
        Generates code based on the provided `diagram` object.

        Parameters:
            diagram (Diagram): The diagram object containing the description of the

        Returns:
            str: The generated response from the Gemini API.

        Raises:
            KeyError: If the configuration file does not contain the required keys.
            requests.exceptions.RequestException: If there is an error while making the API request.
        """
        json_code = self.__send_reqest_with_system_instructions(
            diagram.plugin_name, diagram.description
        )
        try:
            json_code = json.loads(json_code)
            return JSONResponse(content=json_code)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=530, detail="Invalid response from Gemini API"
            )

    def send_message(self, message: Message):
        """
        Sends a message to the Gemini API to generate code based on the provided message.

        Gemini does not handle context as we want, so chats with a context is not supported.
        Even if files are given, it will not be used.

        Parameters:
            message (Message): The message object containing the description of the code to be generated.

        Returns:
            JSONResponse: The generated response from the Gemini API.
        """
        if message.files is not None:
            return JSONResponse(content={"context": "no context"})

        response = self.__send_reqest_with_system_instructions(
            message.plugin_name, message.message, "message"
        )
        json_code = {"message": response}
        json_code["context"] = "no context"
        return JSONResponse(content=json_code)
