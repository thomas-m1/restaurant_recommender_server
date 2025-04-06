from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.core import init_app


app = FastAPI(
    title="Bain Restaurant Recommender",
    version="1.0",
    description="MVP for Bain Partners to find client appropriate restaurants"
)

init_app(app)

app.include_router(api_router, prefix="/api/v1")
