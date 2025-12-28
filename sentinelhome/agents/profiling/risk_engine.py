# sentinelhome/agents/profiling/risk_engine.py

DANGEROUS_PORTS = {
    23: 40,    # Telnet (very risky)
    554: 25,   # RTSP (camera streams)
    22: 15,    # SSH
    1883: 20,  # MQTT (unencrypted)
}

VENDOR_RISK = {
    "unknown": 20,
    "generic": 15,
}

def calculate_port_risk(open_ports):
    risk = 0
    reasons = []

    for port in open_ports:
        if port in DANGEROUS_PORTS:
            risk += DANGEROUS_PORTS[port]
            reasons.append(f"Open dangerous port {port}")

    return risk, reasons


def calculate_vendor_risk(vendor):
    vendor_lower = vendor.lower()
    for key in VENDOR_RISK:
        if key in vendor_lower:
            return VENDOR_RISK[key], [f"Untrusted vendor: {vendor}"]

    return 5, ["Known vendor"]


def calculate_exposure_risk(open_ports):
    count = len(open_ports)
    if count >= 5:
        return 30, ["High number of open ports"]
    elif count >= 3:
        return 15, ["Moderate number of open ports"]
    else:
        return 5, ["Low exposure"]


def compute_device_risk(device):
    total_risk = 0
    reasons = []

    port_risk, port_reasons = calculate_port_risk(device["open_ports"])
    vendor_risk, vendor_reasons = calculate_vendor_risk(device["vendor"])
    exposure_risk, exposure_reasons = calculate_exposure_risk(device["open_ports"])

    total_risk += port_risk + vendor_risk + exposure_risk
    reasons.extend(port_reasons + vendor_reasons + exposure_reasons)

    if total_risk >= 70:
        level = "HIGH"
    elif total_risk >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": total_risk,
        "risk_level": level,
        "risk_reasons": reasons
    }
