import scapy.all as scapy
import socket
import json


def get_local_subnet():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = ".".join(local_ip.split(".")[:-1]) + ".0/24"
    return subnet


def arp_scan(subnet):
    arp_request = scapy.ARP(pdst=subnet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    answered = scapy.srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices


if __name__ == "__main__":
    subnet = get_local_subnet()
    print(f"[+] Scanning subnet: {subnet}")

    devices = arp_scan(subnet)

    print("[+] Devices Found:")
    print(json.dumps(devices, indent=2))
