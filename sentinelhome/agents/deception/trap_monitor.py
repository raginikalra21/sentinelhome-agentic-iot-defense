import time
import os

LOG_FILE = "sentinelhome/data/honeypot_hits.log"


def monitor_traps():
    print("[MONITOR] Deception trap monitor started")

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if line:
                print(f"[ALERT] DECEPTION TRIGGERED → {line.strip()}")
            else:
                time.sleep(1)


if __name__ == "__main__":
    monitor_traps()
