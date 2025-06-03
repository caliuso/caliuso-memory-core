import os
import time
import subprocess
import requests
from datetime import datetime

# Configuration
TELEGRAM_TOKEN = "7711490050:AAESiVBTAjBY0aCyvH1iSysAmmH1hFjKuOg"
TELEGRAM_CHAT_ID = "1259824379"
SYNC_INTERVAL = 600  # Sync every 10 minutes
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

def notify_telegram(message):
    """
    Sends a message to the configured Telegram chat.
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        with open("autosync_error.log", "a") as f:
            f.write(f"{datetime.utcnow()} - Telegram notification failed: {str(e)}\n")

def autosync():
    """
    Performs git synchronization and sends a Telegram notification upon success.
    """
    os.chdir(REPO_PATH)
    while True:
        try:
            # Stage all changes
            subprocess.run(["git", "add", "."], check=True)

            # Commit changes
            commit_message = f"🔁 Auto-sync update {datetime.utcnow().isoformat()}"
            subprocess.run(["git", "commit", "-m", commit_message], check=False)

            # Push to origin
            subprocess.run(["git", "push", "origin", "main"], check=True)

            # Push to mirror
            subprocess.run(["git", "push", "--mirror", "mirror"], check=True)

            # Send Telegram notification
            notify_telegram(f"✅ Auto-sync completed at {datetime.utcnow().isoformat()}")

        except subprocess.CalledProcessError as e:
            with open("autosync_error.log", "a") as f:
                f.write(f"{datetime.utcnow()} - Git operation failed: {str(e)}\n")
        except Exception as e:
            with open("autosync_error.log", "a") as f:
                f.write(f"{datetime.utcnow()} - Unexpected error: {str(e)}\n")

        # Wait before next sync
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    autosync()
