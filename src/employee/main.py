from fastapi import FastAPI
from employee.config import settings

app = FastAPI(title="Employee Portal")

@app.get("/")
def read_root():
     return {"message": f"Hello from {settings.app_name}"}