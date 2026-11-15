from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from employee.config import settings
from employee.logging_config import setup_logging
from employee.middleware import logging_and_error_middleware, rate_limit_middleware
from employee.routers import employee

setup_logging()

app = FastAPI(title=settings.app_name)

app.middleware("http")(rate_limit_middleware)
app.middleware("http")(logging_and_error_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)