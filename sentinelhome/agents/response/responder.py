import time
import re
from sentinelhome.agents.response.firewall import block_ip

LOG_FILE = "sentinelhome/data/honeypot_hits.log"
IP_REGEX = r"\('([\d\.]+)',"


def extract_ip(log_line):
    match = re.search(IP_REGEX, log_line)
    return match.group(1) if match else None


def run_responder():
    print("[RESPONSE] Autonomous response agent started")

    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)  # follow new lines only

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            ip = extract_ip(line)
            if not ip:
                continue

            # ✅ Demo-safe mode: do NOT block localhost
            if ip == "127.0.0.1":
                print("[RESPONSE] Demo mode: skipping localhost block")
                continue

            print(f"[RESPONSE] Blocking attacker IP: {ip}")
            success = block_ip(ip)

            if success:
                print(f"[RESPONSE] IP {ip} blocked successfully")


if __name__ == "__main__":
    run_responder()
