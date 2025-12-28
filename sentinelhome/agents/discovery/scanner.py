import scapy.all as scapy
import socket
import json

from sentinelhome.agents.discovery.device_fingerprint import get_vendor
from sentinelhome.agents.profiling.risk_engine import compute_device_risk

COMMON_IOT_PORTS = [22, 23, 80, 443, 554, 1883, 8883]


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
    for _, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices


def port_scan(ip):
    open_ports = []

    for port in COMMON_IOT_PORTS:
        pkt = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="S")
        resp = scapy.sr1(pkt, timeout=0.5, verbose=False)

        if resp and resp.haslayer(scapy.TCP):
            if resp.getlayer(scapy.TCP).flags == 0x12:
                open_ports.append(port)
                scapy.sr(
                    scapy.IP(dst=ip) / scapy.TCP(dport=port, flags="R"),
                    timeout=0.5,
                    verbose=False
                )

    return open_ports


def infer_device_type(vendor, ports):
    vendor = vendor.lower()

    if 554 in ports:
        return "IP Camera"
    if "tp-link" in vendor or "netgear" in vendor:
        return "Router / Network Device"
    if 1883 in ports or 8883 in ports:
        return "IoT Sensor / Smart Device"
    if 80 in ports or 443 in ports:
        return "Smart Appliance"

    return "Unknown Device"


def main():
    subnet = get_local_subnet()
    print(f"[+] Scanning subnet: {subnet}")

    raw_devices = arp_scan(subnet)
    final_devices = []

    for device in raw_devices:
        vendor = get_vendor(device["mac"])
        ports = port_scan(device["ip"])
        device_type = infer_device_type(vendor, ports)

        risk = compute_device_risk({
            "vendor": vendor,
            "open_ports": ports
        })

        final_devices.append({
            "ip": device["ip"],
            "mac": device["mac"],
            "vendor": vendor,
            "open_ports": ports,
            "device_type": device_type,
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "risk_reasons": risk["risk_reasons"]
        })

    print(json.dumps(final_devices, indent=2))

    with open("sentinelhome/data/devices.json", "w") as f:
        json.dump(final_devices, f, indent=2)


if __name__ == "__main__":
    main()
