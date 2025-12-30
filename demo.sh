#!/bin/bash

echo "🔐 SentinelHome — One Command Demo"
echo "---------------------------------"

echo "[+] Resetting firewall (macOS safe demo)"
sudo pfctl -F all -f /etc/pf.conf >/dev/null 2>&1
sudo pfctl -d >/dev/null 2>&1

echo "[+] Activating virtual environment"
source venv/bin/activate

echo "[+] Starting Fake Router Honeypot"
sudo python sentinelhome/agents/deception/fake_devices/fake_router.py &
ROUTER_PID=$!

sleep 2

echo "[+] Starting Trap Monitor"
python sentinelhome/agents/deception/trap_monitor.py &
MONITOR_PID=$!

sleep 2

echo "[+] Starting Autonomous Response Agent"
sudo python -m sentinelhome.agents.response.responder &
RESPONDER_PID=$!

sleep 2

echo "[+] Starting Dashboard"
uvicorn sentinelhome.dashboard.app:app --reload &
DASHBOARD_PID=$!

echo ""
echo "✅ SentinelHome is running"
echo "🌐 Dashboard: http://127.0.0.1:8000/ui"
echo "🎭 Fake Router: http://localhost:8080/admin"
echo ""
echo "Press CTRL+C to stop all components"

wait
