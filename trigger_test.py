import requests

resp = requests.post("http://localhost:8000/storeMemory", json={
    "session_id": "default",
    "data": "🛠️ ERROR: Fake Enum Test | ✅ SOLUTION: Use shape.triangleup | LAW CODE 999"
})
print(resp.status_code, resp.json())
