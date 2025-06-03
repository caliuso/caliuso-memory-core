import os
from datetime import datetime
import subprocess
import hashlib

IMMORTAL_VAULT = "immutable_vault"
os.makedirs(IMMORTAL_VAULT, exist_ok=True)

def write_and_sign_law(session_id: str, law_text: str):
    timestamp = datetime.utcnow().isoformat()
    filename_raw = f"{session_id}_{timestamp}.law.txt"
    path_raw = os.path.join(IMMORTAL_VAULT, filename_raw)
    
    # Write plaintext LAW
    with open(path_raw, "w") as f:
        f.write(f"LAW ENTRY\nTimestamp: {timestamp}\nSession: {session_id}\n\n{law_text}\n")

    # GPG sign
    signed_file = path_raw + ".asc"
    try:
        subprocess.run(["gpg", "--armor", "--output", signed_file, "--sign", path_raw], check=True)
        print(f"🧬 LAW SIGNED TO VAULT: {signed_file}")
    except subprocess.CalledProcessError:
        print("❌ GPG signing failed. Is GPG setup with a keypair?")

    # Optional hash/log
    hash = hashlib.sha256(law_text.encode()).hexdigest()
    with open(os.path.join(IMMORTAL_VAULT, "ledger_hash"), "a") as f:
        f.write(f"{timestamp} | {session_id} | SHA256: {hash}\n")

    return signed_file

# Example manual call:
if __name__ == "__main__":
    sid = "default"
    law = "ERROR: Reserved keyword used | SOLUTION: Use safe name like entryTrigger | LAW CODE: 001"
    write_and_sign_law(sid, law)
