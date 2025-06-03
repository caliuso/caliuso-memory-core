import re
import matplotlib.pyplot as plt
from datetime import datetime

LAW_FILE = "Marks_Coding_Handbook_Bible_v2025.txt"
OUT_IMAGE = "law_index_chart.png"

def extract_laws(text):
    pattern = r"LAW CODE\s*(\d+)"
    return sorted(set(map(int, re.findall(pattern, text))))

def generate_chart(laws):
    plt.figure(figsize=(10, 5))
    plt.plot(laws, marker='o', linestyle='-', label='Discovered Laws')
    plt.title(f'CALIUSO LAW INDEX ({len(laws)} Laws)')
    plt.xlabel('Index')
    plt.ylabel('LAW CODE')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_IMAGE)
    print(f"✅ LAW chart saved to {OUT_IMAGE}")

if __name__ == "__main__":
    if not os.path.exists(LAW_FILE):
        print("❌ LAW file not found.")
    else:
        with open(LAW_FILE, "r", encoding="utf-8") as f:
            laws = extract_laws(f.read())
            generate_chart(laws)
