from fastapi import FastAPI, Request
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_FILE = 'memory.json'

@app.post("/memory/store")
async def store_memory(request: Request):
    data = await request.json()
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f)
    return {"status": "stored"}

@app.get("/memory/fetch")
async def fetch_memory(session_id: str = ""):
    try:
        with open(MEMORY_FILE, 'r') as f:
            memory = json.load(f)
            return memory
    except FileNotFoundError:
        return {}

@app.delete("/memory/clear")
async def clear_memory(session_id: str = ""):
    open(MEMORY_FILE, 'w').close()
    return {"status": "cleared"}
