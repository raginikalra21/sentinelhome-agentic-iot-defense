from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI(title="SentinelHome Dashboard")

DATA_DIR = "sentinelhome/data"
DEVICES_FILE = os.path.join(DATA_DIR, "devices.json")
HONEYPOT_LOG = os.path.join(DATA_DIR, "honeypot_hits.log")


@app.get("/")
def root():
    return {"status": "SentinelHome Dashboard running"}


@app.get("/devices")
def get_devices():
    if not os.path.exists(DEVICES_FILE):
        return []
    with open(DEVICES_FILE) as f:
        return json.load(f)


@app.get("/alerts")
def get_alerts():
    if not os.path.exists(HONEYPOT_LOG):
        return []
    with open(HONEYPOT_LOG) as f:
        return f.readlines()


@app.get("/ui", response_class=HTMLResponse)
def dashboard_ui():
    return """
    <html>
    <head>
        <title>SentinelHome Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #020617;
                color: #e5e7eb;
                margin: 0;
                padding: 30px;
            }
            h1 {
                color: #38bdf8;
                margin-bottom: 5px;
            }
            .legend {
                color: #94a3b8;
                margin-bottom: 30px;
                font-size: 14px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #1e293b;
                text-align: left;
                font-size: 14px;
            }
            th {
                color: #94a3b8;
                font-weight: normal;
            }
            .badge-low { color: #22c55e; font-weight: bold; }
            .badge-medium { color: #eab308; font-weight: bold; }
            .badge-high { color: #ef4444; font-weight: bold; }
            .card {
                background: #020617;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 30px;
            }
            .alert {
                color: #f87171;
                font-family: monospace;
                font-size: 13px;
                margin-bottom: 8px;
            }
        </style>
    </head>

    <body>

        <h1>SentinelHome Security Dashboard</h1>
        <div class="legend">
            🟢 LOW: Known vendor & minimal exposure &nbsp;&nbsp;
            🟡 MEDIUM: Unknown device or limited exposure &nbsp;&nbsp;
            🔴 HIGH: Active attack surface or deception trigger
        </div>

        <div class="card">
            <h2>IoT Devices</h2>
            <table id="deviceTable">
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>Vendor</th>
                        <th>Device Type</th>
                        <th>Open Ports</th>
                        <th>Risk Level</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <div class="card">
            <h2>Deception Alerts</h2>
            <div id="alerts">Loading alerts...</div>
        </div>

        <div class="card">
            <h2>Autonomous Actions</h2>
            <div id="actions">No actions taken yet.</div>
        </div>

        <script>
            function riskBadge(level) {
                if (level === "HIGH") return "<span class='badge-high'>HIGH</span>";
                if (level === "MEDIUM") return "<span class='badge-medium'>MEDIUM</span>";
                return "<span class='badge-low'>LOW</span>";
            }

            function loadDevices() {
                fetch('/devices')
                    .then(res => res.json())
                    .then(devices => {
                        const tbody = document.querySelector("#deviceTable tbody");
                        tbody.innerHTML = "";
                        devices.forEach(d => {
                            const row = document.createElement("tr");
                            row.innerHTML = `
                                <td>${d.ip}</td>
                                <td>${d.vendor}</td>
                                <td>${d.device_type}</td>
                                <td>${(d.open_ports || []).join(", ")}</td>
                                <td>${riskBadge(d.risk_level)}</td>
                            `;
                            tbody.appendChild(row);
                        });
                    });
            }

            function loadAlerts() {
                fetch('/alerts')
                    .then(res => res.json())
                    .then(alerts => {
                        const alertDiv = document.getElementById("alerts");
                        alertDiv.innerHTML = "";

                        alerts.slice(-10).reverse().forEach(a => {
                            const p = document.createElement("div");
                            p.className = "alert";
                            p.innerText = a;
                            alertDiv.appendChild(p);
                        });

                        const actionDiv = document.getElementById("actions");
                        if (alerts.length > 0) {
                            actionDiv.innerHTML = `
                                🔒 Action: Attacker blocked<br/>
                                📍 Reason: Deception trap triggered<br/>
                                🕒 ${alerts[alerts.length - 1]}
                            `;
                        }
                    });
            }

            loadDevices();
            loadAlerts();
            setInterval(loadAlerts, 5000);
        </script>

    </body>
    </html>
    """
