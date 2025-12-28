import socket
import datetime

LOG_FILE = "sentinelhome/data/honeypot_hits.log"


def log_attack(addr):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] RTSP connection from {addr}\n")


def start_fake_camera(host="0.0.0.0", port=554):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[HONEYPOT] Fake IP Camera listening on port {port}")

    while True:
        client, addr = server.accept()
        print(f"[ALERT] Honeypot hit from {addr}")
        log_attack(addr)
        client.close()


if __name__ == "__main__":
    start_fake_camera()
