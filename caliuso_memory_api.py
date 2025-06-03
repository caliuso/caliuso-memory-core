from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
import os
from datetime import datetime

app = FastAPI()

class MemoryEntry(BaseModel):
    session_id: str
    data: str

memory_dir = "memory_grid"
os.makedirs(memory_dir, exist_ok=True)

@app.post("/storeMemory")
def store_memory(entry: MemoryEntry):
    path = os.path.join(memory_dir, f"{entry.session_id}.json")
    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": entry.data
    }
    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)
    else:
        history = []
    history.append(new_entry)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)
    return {"status": "stored", "entry_count": len(history)}

@app.post("/fetchMemory")
def fetch_memory(payload: dict):
    session_id = payload["session_id"]
    path = os.path.join(memory_dir, f"{session_id}.json")
    if not os.path.exists(path):
        return {"memory": []}
    with open(path) as f:
        return {"memory": json.load(f)}

@app.get("/logs/{session_id}")
def get_log(session_id: str):
    path = os.path.join(memory_dir, f"{session_id}.json")
    if not os.path.exists(path):
        return {"log": []}
    with open(path) as f:
        return {"log": json.load(f)}

@app.post("/init")
def init_session(payload: dict):
    session_id = payload["session_id"]
    path = os.path.join(memory_dir, f"{session_id}.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
    return {"status": "initialized"}
