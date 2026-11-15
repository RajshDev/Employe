from fastapi import FastAPI
from employee.config import settings
from employee.routers import employee

app = FastAPI(title=settings.app_name)

app.include_router(employee.router)