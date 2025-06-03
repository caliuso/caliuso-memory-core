from fastapi import FastAPI
from pydantic import BaseModel
import os, json
from datetime import datetime
import requests

app = FastAPI()

RENDER_HOOK = "https://api.render.com/deploy/srv-d0v36afdiees73cf3gqg?key=ndrwqm0sqVI"
memory_dir = "memory_grid"
os.makedirs(memory_dir, exist_ok=True)

class MemoryEntry(BaseModel):
    session_id: str
    data: str

@app.post("/storeMemory")
def store_memory(entry: MemoryEntry):
    path = os.path.join(memory_dir, f"{entry.session_id}.json")
    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": entry.data
    }

    history = []
    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)
    history.append(new_entry)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

    if "LAW" in entry.data.upper() or "ERROR:" in entry.data.upper():
        try:
            resp = requests.post(RENDER_HOOK)
            print("🔥 Render Deploy Triggered:", resp.status_code)
            with open("deploy.log", "a") as log_file:
                log_file.write(f"{datetime.utcnow().isoformat()} | Deploy Triggered | Status: {resp.status_code}\n")
        except Exception as e:
            print("⚠️ Webhook failed:", e)

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

@app.get("/status")
def get_status():
    session_id = "default"
    path = os.path.join(memory_dir, f"{session_id}.json")
    memory_log_exists = os.path.exists(path)
    deploy_log_exists = os.path.exists("deploy.log")
    entry_count = 0

    if memory_log_exists:
        with open(path) as f:
            try:
                entry_count = len(json.load(f))
            except:
                entry_count = -1

    return {
        "deploy_log_exists": deploy_log_exists,
        "memory_log_exists": memory_log_exists,
        "session_id": session_id,
        "entry_count": entry_count,
        "timestamp": datetime.utcnow().isoformat()
    }
