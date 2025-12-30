import subprocess
import platform

def block_ip(ip):
    system = platform.system().lower()

    if system == "darwin":
        # macOS (pfctl anchor approach – demo-friendly)
        rule = f"block drop from {ip} to any\n"
        with open("/tmp/sentinel_block.conf", "w") as f:
            f.write(rule)
        subprocess.run(["pfctl", "-ef", "/tmp/sentinel_block.conf"], check=False)
        return True

    elif system == "linux":
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=False)
        return True

    else:
        print(f"[WARN] Unsupported OS for auto-block: {system}")
        return False
