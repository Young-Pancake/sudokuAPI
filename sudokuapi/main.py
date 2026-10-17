from fastapi import FastAPI, Depends
from .routers import database

app = FastAPI()

app.include_router(database.router)

@app.get("/")
async def read_item():
    return {"item": "hello world"}
