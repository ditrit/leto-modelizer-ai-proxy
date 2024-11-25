from fastapi import APIRouter

from src.models.Diagram import Diagram
from src.handlers.Factory import Factory

router = APIRouter(
    prefix="/diagram",
    tags=["diagram"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
def generate(diagram: Diagram):
    """
    Generates code based on the provided `diagram` object.

    Parameters:
        diagram (Diagram): The diagram object containing the description of the diagram.

    Returns:
        str: The generated response from the API.

    Raises:
        KeyError: If the configuration file does not contain the required keys.
        requests.exceptions.RequestException: If there is an error while making the API request.
    """

    print(f"Receive POST /api/diagram request with body: {diagram.dict()}")
    return Factory.get_handler(diagram.plugin_name).generate(diagram)
