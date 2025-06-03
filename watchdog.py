# immortal_watchdog.py

import subprocess
import time
import os

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
API_CMD = ["python", "-m", "uvicorn", "caliuso_memory_api:app", "--host", "0.0.0.0", "--port", "8000"]

def run_server():
    while True:
        try:
            # 🧠 AUTO-PULL LATEST REPO
            subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True)

            # 🔗 CHAIN AUTOSYNC
            subprocess.Popen(["python", "autosync.py"], cwd=REPO_PATH)

            # 🚀 BOOT API SERVER
            proc = subprocess.Popen(API_CMD, cwd=REPO_PATH)
            proc.wait()
        except Exception as e:
            with open("watchdog_crash.log", "a") as f:
                f.write(f"[CRASH] {time.ctime()} - {str(e)}\n")
        time.sleep(5)

if __name__ == "__main__":
    run_server()
