# 🛡️ CyberPulse — Cyber Risk Quantification Dashboard

> **Quantifying organizational cyber risk exposure through vulnerability analysis and financial impact estimation.**  
> A cybersecurity analytics project that translates CVSS vulnerability data into business-language risk intelligence — built for analysts, presented for executives.

---

## 📌 Project Overview

CyberPulse is a cybersecurity analytics project that ingests vulnerability data, applies a risk scoring model based on CVSS severity, estimates financial exposure, and surfaces findings through an executive-ready Power BI dashboard.

The core question this project answers:

**"What is the estimated financial impact of our organization's current vulnerability landscape?"**

Total exposure identified: **$185,000,000** across scored risk categories.

---

## 📊 Dashboard Preview

> *(Add Power BI screenshot here)*

---

## 🏗️ Project Workflow

```
Raw Vulnerability Data
        │
        ▼
┌──────────────────────┐
│   Python ETL Layer   │  ← cyber_risk_analysis.ipynb
│  Data cleaning,      │
│  enrichment, prep    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   Risk Scoring       │  ← CVSS-based severity scoring
│   Engine             │     weighted by vulnerability
│                      │     distribution and frequency
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Financial Exposure  │  ← Severity-weighted exposure
│  Estimation          │     estimation model
│  ($185M total)       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  cyber_risk_final    │  ← Clean, analysis-ready dataset
│       .csv           │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Power BI Dashboard  │  ← cyberPulse_dashboard.pbix
│  Executive KPIs,     │
│  risk breakdowns,    │
│  visual storytelling │
└──────────────────────┘
```

---

## 📂 Repository Structure

```
cyberPulse-threat-intelligence/
│
├── 📓 cyber_risk_analysis.ipynb   # ETL, risk scoring, and exposure estimation
├── 📊 cyberPulse_dashboard.pbix   # Power BI executive dashboard
├── 📁 data/
│   └── cyber_risk_final.csv       # Cleaned dataset output
├── 📁 screenshots/                # Dashboard screenshots
└── 📄 README.md
```

---

## ⚙️ What This Project Does

| Component | What It Actually Does |
|---|---|
| 🔄 **ETL Pipeline** | Loads, cleans, and structures raw vulnerability data using Python and Pandas |
| 🎯 **Risk Scoring** | Scores vulnerabilities using CVSS severity levels and frequency distribution |
| 💰 **Exposure Estimation** | Estimates financial exposure by weighting risk scores against assumed asset values |
| 📊 **Power BI Dashboard** | Visualizes KPIs, risk distribution, and exposure breakdown for non-technical stakeholders |
| 📁 **Data Export** | Produces a clean CSV ready for reporting or further analysis |

---

## 🔢 Key Findings

- 💥 **Total Estimated Exposure:** $185,000,000
- 🔴 **Critical Vulnerabilities:** *(add count)*
- 🟠 **High Severity Vulnerabilities:** *(add count)*
- 📋 **Total Records Analyzed:** *(add count)*
- 📅 **Dataset Period:** *(add date range)*

---

## 🛠️ Tech Stack

| Layer | Tools Used |
|---|---|
| **Data Processing** | Python, Pandas, NumPy |
| **Risk Scoring Logic** | CVSS-based custom scoring in Python |
| **Visualization** | Power BI Desktop |
| **Notebook Environment** | Jupyter Notebook |
| **Data Format** | CSV |

---

## 📖 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/cyberPulse-threat-intelligence.git
cd cyberPulse-threat-intelligence
```

### 2. Install Python Dependencies
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 3. Run the Notebook
```bash
jupyter notebook cyber_risk_analysis.ipynb
```
Run all cells — the notebook processes the data, applies risk scoring, and exports `cyber_risk_final.csv`.

### 4. Open the Dashboard
Open `cyberPulse_dashboard.pbix` in **Power BI Desktop** and refresh the data source to point to your local `cyber_risk_final.csv`.

---

## 📊 Dashboard Highlights

- **Executive Summary** — Total exposure, risk score distribution, vulnerability counts by severity
- **Risk Breakdown** — CVSS severity distribution across asset/category groups
- **Exposure Estimation** — Financial impact by risk tier
- **Vulnerability Trends** — Distribution patterns across the dataset
- **Top Risk Areas** — Highest-exposure categories ranked by estimated impact

---

## 💡 Design Decisions & Limitations

This project is intentionally scoped as an **analytics and visualization project**, not a production security tool.

A few honest notes:

- **Financial exposure figures** are estimated using a severity-weighted scoring model — not actuarial or insurance-grade calculations. They illustrate relative risk magnitude, not exact dollar values.
- **Risk scoring** is based on CVSS severity bands — a widely used industry standard — rather than a proprietary or ML-based engine.
- **The dataset** is *(describe here: synthetic / sourced from X / anonymized real data)*.

This scoping is intentional. The goal was to build something **honest, explainable, and business-relevant** — not to over-engineer for the sake of complexity.

---

## 🔭 Future Roadmap

- [ ] Integrate live CVE feeds for real-time vulnerability ingestion
- [ ] Add asset criticality weighting to the scoring model
- [ ] Automate the ETL pipeline with scheduling (Airflow / Task Scheduler)
- [ ] Deploy to Power BI Service for live sharing
- [ ] Explore ML-based risk clustering across vulnerability categories

---

## 👤 Author

**Reshmitha** — *Cybersecurity & Data Analytics*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/YOUR_USERNAME)

---



---

> *"Good security analytics doesn't just find risk — it helps leadership understand what that risk costs."*
