import requests

res = requests.post("http://localhost:8000/storeMemory", json={
    "session_id": "default",
    "data": "🛠️ ERROR: Invalid enum | ✅ SOLUTION: Use shape.triangleup | LAW CODE 007"
})

print(res.status_code)
print(res.json())
