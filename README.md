# 🔔 Vendor Monitoring & Slack Alert Automation Toolkit

A real-time monitoring toolkit designed to automate file delivery checks and Slack alert triage in a trading technology environment. Built in Python using the Slack SDK and custom API integrations to reduce manual support load.

## 📘 Project Description

This project was created to help streamline and automate tasks traditionally handled by application support teams in a financial trading environment. It contains two tools:

1. **Vendor File Delivery Monitor** – Polls an API to verify the timely delivery of vendor files, and sends alerts to Slack/Incident.io if something is missing.
2. **Slack Message Monitor** – Listens to Slack channels in real time and reacts to production error messages or user mentions by alerting the right teams.

This toolkit solves repetitive and error-prone tasks typically done during SOD (Start-of-Day) and EOD (End-of-Day) checks, helping reduce human mistakes, delay, and alert fatigue.

## 📚 Table of Contents

1. [Installation and Technologies Used](#installation-and-technologies-used)
2. [How to Use](#how-to-use)
3. [Folder Structure](#folder-structure)
4. [Other Note](#other-note)
5. [Why This Project Was Built](#why-this-project-was-built)

---

## 🧰 Installation and Technologies Used

Technologies Used

- **Python 3** – Core scripting language
- **Slack Bolt SDK** – Event-driven Slack bot framework
- **Incident.io** (via webhook) – For structured incident alerts
- `requests`, `requests-kerberos` – Secure API calls to vendor endpoints
- `dotenv` – Load environment-based secrets and configs
- `logging` – Built-in structured logging for debugging and visibility

Clone the repo:

```bash
git clone https://github.com/your-username/vendor-monitoring-tools.git
cd vendor-monitoring-tools
```

## 🚀 How to Use

### 1. Check that vendor files have sent:

```bash
python scripts/file_monitor.py
```

#### Workflow:

- Calls the vendor's API securely
- Parses file names based on time and endpoint
- Alerts via Slack or Incident.io if anything is missing or delayed

### 2. Slack Monitoring Script

Listen to real-time Slack events and auto-respond:

```bash
python scripts/slack_msg_monitor.py
```

#### Workflow:

- Monitors multiple Slack channels
- Detects keywords like failed, critical, or custom ones
- Re-tags team members or raises alerts automatically with context

## 🗂 Folder Structure

```bash
vendor-monitoring-tools/
│
├── config/
│   ├── call_env_variable.py
│   ├── mappings.py
│   └── .env
│
├── main_scripts/
│   ├── file_monitor.py           # File delivery monitor
│   └── slack_msg_monitor.py      # Slack listener for triage
│
├── reactions/
│   ├── slack_reaction.py         # Slack alerting utility
│   └── incidentio_reaction.py    # Incident.io alert utility
│
├── requirements.txt
└── README.md
```

## 🔐 Other Note

- Credentials - This project is using dotenv package to handle credentials in .env file, which never be committed to the repository. Use .gitignore to exclude them. Please prepare your own .env which use in this format:

```bash
SLACK_BOT_TOKEN=xoxb-***
SLACK_APP_TOKEN=xapp-***
```

- Security - No real file names, credentials, or production data are included in the public version

## 🧠 Why This Project Was Built

In my previous role supporting production systems, we received a large volume of system-generated messages into a shared Slack channel used for infrastructure alerts. This made it difficult to distinguish routine logs from critical failures — especially during busy hours like start-of-day.

To improve clarity and reduce manual monitoring, I developed a bot that:

- Filters incoming messages for error patterns
- Sends alerts to the right support team or on-call group
- Generates direct links to the original message for rapid triage

I also created a script to verify vendor file deliveries via API and proactively notify support when expected files were missing — improving SOD readiness and reducing firefighting.

- Monitor vendor file deliveries via API
- Detect delays or missing files
- Proactively notify support channels to follow up

---

## ✅ Benefits

- Automated noisy Slack alert channel triage
- Improved response time for production issues
- Improved SOD handoff with early detection of vendor file issues
- Reusable logic for different environments (e.g., staging, production, risk)
