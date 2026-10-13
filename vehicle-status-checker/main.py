from fastapi import FastAPI, HTTPException

app = FastAPI()

items = [
    {"item_id": 1, "q": "query1"},
    {"item_id": 2, "q": "query2"},
]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    for item in items:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")