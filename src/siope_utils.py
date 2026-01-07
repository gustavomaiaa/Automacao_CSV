import os
from datetime import datetime

def log(msg, arquivo_log="logs/execucao.log"):
    os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)