import subprocess
from datetime import datetime

# ⏳ Timestamp snapshot for versioning
timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

# ✅ Stage critical files
subprocess.call("git add deploy.log trace.log ledger_hash.txt", shell=True)

# 🧠 Append commit message w/ timestamp
commit_msg = f'🧠 IMMORTAL LOG SYNC — {timestamp}'
subprocess.call(f'git commit -m "{commit_msg}"', shell=True)

# 🚀 Push to GitHub
subprocess.call("git push origin main", shell=True)
