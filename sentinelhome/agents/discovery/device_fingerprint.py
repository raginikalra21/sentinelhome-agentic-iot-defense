import requests

def get_vendor(mac):
    """
    Lookup vendor using MAC address
    """
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass

    return "Unknown Vendor"
