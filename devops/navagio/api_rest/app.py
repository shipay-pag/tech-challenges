from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def read_root():
    return {"Hello": "Shipay"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}