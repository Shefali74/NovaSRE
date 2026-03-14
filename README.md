# NovaSRE - Autonomous Cloud Self-Healing System

NovaSRE is an AI-powered cloud reliability simulation dashboard that detects service degradation, identifies potential root causes, and executes automated mitigation for critical incidents.

This project demonstrates how Site Reliability Engineering (SRE) workflows can be enhanced using autonomous monitoring, AI-based reasoning, and self-healing actions in a cloud-inspired service environment.


## Problem Statement

Modern cloud systems are highly interconnected. A failure in one service, especially a database bottleneck, can cascade into API latency, payment failures, and revenue loss.

Traditional monitoring dashboards only show metrics. They do not actively reason about the issue or trigger mitigation automatically.

NovaSRE solves this by simulating:

- live infrastructure telemetry
- early warning detection
- critical incident identification
- AI-generated root cause reasoning
- autonomous mitigation
- service recovery tracking


## Key Features

- **Live Metric Simulation**
  - Continuously generates cloud service telemetry such as CPU usage, database load, latency, payment error rate, and revenue throughput.

- **Incident Detection Engine**
  - Detects both warning and critical states using threshold-based logic.

- **AI Root Cause Reasoning**
  - Uses Amazon Nova via AWS Bedrock to generate structured technical reasoning for incidents.

- **Autonomous Mitigation**
  - Simulates self-healing actions such as scaling database resources and optimizing connection pooling.

- **Dependency Graph Visualization**
  - Shows service relationships and highlights incident propagation across the system.

- **Recovery Tracking**
  - Confirms when the system stabilizes and logs recovery events.

- **Event Log Timeline**
  - Displays warnings, incidents, AI reasoning completion, mitigation actions, and recovery messages.


## Architecture Overview

NovaSRE simulates this cloud dependency flow:

`User Traffic → API Service → Database → Payment Service → Revenue System`

A database saturation issue can propagate downstream and affect payment processing and business revenue.


## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **NetworkX**
- **Matplotlib**
- **AWS Bedrock**
- **Amazon Nova Lite**
- **Boto3**


## Project Structure

NovaSRE/
│
├── agents/
│   ├── detection_agent.py
│   ├── reasoning_agent.py
│   ├── execution_agent.py
│   └── dependency_agent.py
│
├── utils/
│   └── simulation.py
│
├── data/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md