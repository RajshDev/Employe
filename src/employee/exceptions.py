import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("employee")

class AppError(Exception):
    status_code = 500
    message = "Something went wrong"

class EmployeeNotFoundError(AppError):
    status_code = 404
    message = "Employee not found"

class EmployeeAlreadyExistsError(AppError):
    status_code = 400
    message = "Employee already exists"

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "error": "Invalid input", "details": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        logger.exception(f"{request.method} {request.url.path} failed")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Something went wrong"},
        )