from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import os
import json

app = FastAPI()

MEMORY_FILE = "immortal_memory.json"

# Create file if not exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

class MemoryEntry(BaseModel):
    error: str
    context: str
    symptom: str
    solution: str
    result: str
    handbook_date: str

@app.post("/storeMemory")
async def store_memory(entry: MemoryEntry):
    with open(MEMORY_FILE, "r") as f:
        memory_data = json.load(f)

    # Append new entry
    memory_data.append(entry.dict())

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_data, f, indent=4)

    return {"status": "IMMORTAL LAW LOGGED", "entry": entry.dict()}

@app.get("/status")
async def status():
    return {
        "status": "IMMORTAL ONLINE",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/memory")
async def read_memory():
    with open(MEMORY_FILE, "r") as f:
        memory_data = json.load(f)
    return memory_data
