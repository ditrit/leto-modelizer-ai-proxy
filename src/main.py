from fastapi import APIRouter, FastAPI

from src.routers import diagram, message, configuration

app = FastAPI()

# Create a parent router with the prefix "/api"
api_router = APIRouter(prefix="/api")

api_router.include_router(configuration.router)
api_router.include_router(diagram.router)
api_router.include_router(message.router)

app.include_router(api_router)


@app.get("/")
async def root() -> dict:
    """
    This endpoint is the entrypoint of the API and returns a welcome message.
    """
    return {"message": "Hello From Leto-Modelizer-AI-API!"}


@app.get("/health")
async def root() -> dict:
    """
    This endpoint is the entrypoint of the API and returns a diagnostic message.
    """
    return {"status": "ok", "version": "1.0.0"}
