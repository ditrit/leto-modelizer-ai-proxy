from fastapi import APIRouter, FastAPI

from src.routers import diagram
from src.handlers.Factory import Factory

app = FastAPI()

# Create a parent router with the prefix "/api"
api_router = APIRouter(prefix="/api")

api_router.include_router(diagram.router)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """
    This function is called when the API starts.

    It initializes the API by calling the `initialize` method of the `Factory` class
    which initializes all the models defined in the configuration file.
    """
    print("Initializing the API...")
    Factory.initialize_models()


@app.get("/")
async def root() -> dict:
    """
    This endpoint is the entrypoint of the API and returns a welcome message.
    """
    return {"message": "Hello From Leto-Modelizer-AI-API!"}
