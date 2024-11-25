from typing import Annotated
from requests.exceptions import RequestException

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from src.configuration.configurationManager import ConfigurationManager
from src.handlers.Factory import Factory

router = APIRouter(
    prefix="/configurations",
    tags=["configurations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get-configuration")
def get_configuration():
    """
    Endpoint to retrieve the configuration.
    Ensures the configuration is properly set before being accessed.
    """
    try:
        configuration_manager = ConfigurationManager()

        # Retrieve the configuration after ensuring it is set
        config = configuration_manager.get_configuration()

        return JSONResponse(
            content={"configuration": config}
        )  # Assuming you want to return the decoded config

    except ValueError as e:
        return JSONResponse(
            content={"status": "error", "detail": "Failed to save configuration"},
            status_code=500,
        )


@router.post("")
async def save_configuration(request: Request):
    """
    Saves the provided encrypted `configuration` data to the configuration file.

    Parameters:
        configuration (bytes): The encrypted configuration data to save.

    Returns:
        JSONResponse: A JSON object with the status of the save operation.

    Raises:
        HTTPException: If a KeyError or RequestException occurs during saving.
    """
    try:
        encrypted_data: bytes = await request.body()  # Encrypted binary data
        print("Received POST /api/configuration request with encrypted body")

        # Synchronously access the singleton with a lock to avoid race conditions
        configuration_manager = ConfigurationManager()
        await configuration_manager.set_configuration(encrypted_data)

        return JSONResponse(content={"status": "success"}, status_code=201)

    except RequestException:
        return JSONResponse(
            content={"status": "error", "detail": "Failed to save configuration"},
            status_code=500,
        )


@router.post("/initialize")
def initialize(handler: Annotated[set[str] | None, Query()] = None):
    """
    Initializes all the models defined in the configuration file.

    Parameters:
        handler (set[str] | None, optional): The handler names to initialize. Defaults to None.

    Returns:
        str: The generated response from the API.
    """
    print(
        f"Receive POST /api/configuration/initialize request {'with body:' + str(handler) if handler else ''}"
    )

    responses = Factory.initialize_models(handler)
    return JSONResponse(
        content={"status": "success", "responses": responses}, status_code=201
    )


@router.get("/descriptions")
def get_all_configuration_descriptions():
    """
    Retrieves all the descriptions of the configuration fields used by all the handlers.

    Returns:
        dict: A dictionary with the handler names as keys and the descriptions as values.
    """
    return Factory.get_all_configuration_descriptions()
