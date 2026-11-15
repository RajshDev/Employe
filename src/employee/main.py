from fastapi import FastAPI

app = FastAPI(title="Employee Portal")

@app.get("/")
def read_root():
    return {"message": "Hello from Employee Portal"}