from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
import logging
from app.core.config import settings, ENV_FILE_USED



logger = logging.getLogger("uvicorn")

def init_app(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup():
        global resources
        logger.info("App startup")
        logger.info(f"ENV_FILE: {ENV_FILE_USED}")
        logger.info(f"ENV: {settings.ENV}")
        logger.info(f"VERSION: {settings.APP_VERSION}")
        logger.info(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")


    @app.on_event("shutdown")
    async def on_shutdown():
        logger.info("App shutdown")


    # Error Handling
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "type": "HTTPException"},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": exc.errors(), "type": "ValidationError"},
        )