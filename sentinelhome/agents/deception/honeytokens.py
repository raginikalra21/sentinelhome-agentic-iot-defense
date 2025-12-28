import datetime

HONEYTOKENS = {
    "admin": "admin123",
    "root": "toor",
    "iot_admin": "iot@123"
}

LOG_FILE = "sentinelhome/data/honeypot_hits.log"


def check_honeytoken(username, password, source_ip="unknown"):
    if username in HONEYTOKENS and HONEYTOKENS[username] == password:
        with open(LOG_FILE, "a") as f:
            f.write(
                f"[{datetime.datetime.now()}] "
                f"HONEYTOKEN USED: {username}/{password} "
                f"from {source_ip}\n"
            )
        return True
    return False
