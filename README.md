# SentinelHome 🔐
### Agentic AI–Powered Deceptive Defense for Home IoT Networks

SentinelHome is a **plug-and-play, edge-based security system** that autonomously protects home IoT devices using **agentic AI principles**, **deception technologies**, and **real-time autonomous response**.

Instead of reacting after compromise, SentinelHome **proactively traps attackers** using fake IoT devices (honeypots) and blocks them automatically at the network edge.

---

## 🚨 Problem Statement

Home IoT devices such as smart cameras, routers, TVs, and appliances are:
- Poorly monitored
- Rarely updated
- Easy targets for cyber attacks

Traditional security solutions are:
- Reactive (detect after damage)
- Cloud-dependent (privacy risks)
- Not consumer-friendly

As a result, home users lack **visibility**, **control**, and **real-time protection**.

---

## 💡 Our Solution

SentinelHome acts as an **intelligent security gateway** that:

- Automatically discovers all IoT devices on the home network
- Profiles device risk using explainable security heuristics
- Deploys **deception-based honeypots** (fake camera, fake router)
- Detects attackers with **zero false positives**
- **Autonomously blocks attacker IPs** without user intervention

All processing happens **locally at the edge**, ensuring privacy and low latency.

---

## 🧠 System Architecture (High Level)

## 🧠 System Architecture

```mermaid
flowchart LR
    A[Home IoT Devices<br/>(Camera, Router, TV, Bulbs)] --> B[Device Discovery Agent]
    B --> C[Risk Profiling Engine]

    A --> D[Deception Layer]
    D --> D1[Fake IP Camera]
    D --> D2[Fake Router Admin Panel]
    D --> D3[Honeytokens]

    D --> E[Trap Monitor Agent]
    E --> F[Autonomous Response Agent]
    F --> G[Firewall / IP Blocking]

    C --> H[(Local Data Store)]
    E --> H
    F --> H

    H --> I[Optional Web Dashboard]

Home Network
|
[ SentinelHome Edge System ]
|
| Discovery | Risk Profiling | Deception | Response |



---

## 🔍 Key Features

### 1️⃣ IoT Device Discovery & Risk Profiling
- Automatic network scanning
- Vendor fingerprinting and port analysis
- Explainable risk scoring (LOW / MEDIUM / HIGH)
- Human-readable risk reasons

---

### 2️⃣ Deception-Based Security (Core Innovation)
- Fake IP Camera honeypot (RTSP)
- Fake Router Admin Panel honeypot
- Honeytokens (fake credentials)
- Attackers interact with traps instead of real devices

> Any interaction with a honeypot is treated as high-confidence malicious activity.

---

### 3️⃣ Autonomous Detection & Response
- Real-time trap monitoring
- Automatic extraction of attacker IP
- Autonomous firewall-level IP blocking
- Zero-click defense (no user action required)

---

## ⚙️ Technology Stack

- **Python 3**
- **Agent-based modular architecture**
- **Scapy** (network discovery & packet analysis)
- **Socket programming** (IoT honeypots)
- **HTTPServer** (fake router admin panel)
- **Edge-based execution** (privacy-preserving)

---

## 🧪 Demo Workflow

1. SentinelHome scans and profiles IoT devices
2. Fake IoT devices are deployed on the network
3. Attacker probes router admin page
4. Honeypot detects interaction instantly
5. Trap monitor raises alert
6. Autonomous response agent blocks attacker IP

---

## 🏆 Why SentinelHome is Unique

- Uses **agentic AI concepts**, not just ML
- Deception-first security strategy
- Zero false positives
- Privacy-preserving (no cloud dependency)
- Designed for real-world home users

---

## 🚀 Future Enhancements

- ML-based behavioral anomaly detection
- Fine-grained policy engine
- Real-time web dashboard
- Mobile alerts
- ISP and smart-home integrations

---

## 👥 Team
**Team Name:** PhantomOps

---

## 📜 License
This project is built for hackathon and educational purposes.
