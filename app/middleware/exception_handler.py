"""
Global Exception Handler Middleware.
Intercepts all exceptions and converts them into standard APIResponse JSON format.
Ensures zero internal trace leaks to clients in production.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from app.core.exceptions import BaseAppException
from app.core.logging import logger
from app.core.security import sanitize_log_input
from app.schemas.response import APIResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers on the FastAPI application instance."""

    @app.exception_handler(BaseAppException)
    async def base_app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
        """Handles custom application domain exceptions."""
        logger.warning(
            "Domain Exception [%s]: Path=%s | Message=%s",
            exc.status_code,
            sanitize_log_input(request.url.path),
            sanitize_log_input(exc.message),
        )
        response_body = APIResponse.error_response(
            message=exc.message,
            errors=exc.errors
        ).model_dump()
        return JSONResponse(
            status_code=exc.status_code,
            content=response_body
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handles Pydantic request payload/query validation errors."""
        formatted_errors = []
        for error in exc.errors():
            formatted_errors.append({
                "field": " -> ".join([str(loc) for loc in error.get("loc", [])]),
                "message": error.get("msg", ""),
                "type": error.get("type", "")
            })
        
        logger.info(
            "Validation Error [422]: Path=%s | Errors=%s",
            sanitize_log_input(request.url.path),
            sanitize_log_input(formatted_errors),
        )
        response_body = APIResponse.error_response(
            message="Request validation failed",
            errors=formatted_errors
        ).model_dump()
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response_body
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handles standard FastAPI HTTP exceptions."""
        logger.warning(
            "HTTP Exception [%s]: Path=%s | Detail=%s",
            exc.status_code,
            sanitize_log_input(request.url.path),
            sanitize_log_input(exc.detail),
        )
        response_body = APIResponse.error_response(
            message=str(exc.detail),
            errors=None
        ).model_dump()
        return JSONResponse(
            status_code=exc.status_code,
            content=response_body
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Fallback handler for unexpected system errors."""
        logger.error(
            "Unhandled System Error [500]: Path=%s | Exception=%s: %s",
            sanitize_log_input(request.url.path),
            type(exc).__name__,
            sanitize_log_input(exc),
            exc_info=True
        )
        response_body = APIResponse.error_response(
            message="An internal server error occurred",
            errors=None
        ).model_dump()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response_body
        )
