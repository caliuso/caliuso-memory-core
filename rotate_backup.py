import os, shutil, time
from datetime import datetime

vault = "memory_grid"
backup_dir = "vault_backups"
os.makedirs(backup_dir, exist_ok=True)

ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
backup_name = f"backup_{ts}.zip"
backup_path = os.path.join(backup_dir, backup_name)

shutil.make_archive(backup_path.replace(".zip", ""), 'zip', vault)
print(f"🔁 Encrypted vault snapshot created: {backup_path}")
