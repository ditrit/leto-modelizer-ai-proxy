from fastapi import APIRouter

from src.models.Message import Message
from src.handlers.Factory import Factory

router = APIRouter(
    prefix="/message",
    tags=["message"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
def message(message: Message):
    """
    Generates code based on the provided `message` object.
    It is like a conversation with an AI.

    Parameters:
        message (Message): The message object containing the message to send to the AI.

    Returns:
        str: The generated response from the API.

    Raises:
        KeyError: If the configuration file does not contain the required keys.
        requests.exceptions.RequestException: If there is an error while making the API request.
    """

    print(f"Receive POST /api/message request with body: {message.dict()}")
    return Factory.get_handler(message.plugin_name).send_message(message=message)
