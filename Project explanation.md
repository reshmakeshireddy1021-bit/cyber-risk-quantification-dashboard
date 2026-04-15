# 📋 CyberPulse — Cyber Risk Quantification Dashboard — Project Explanation

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=FF4444&width=600&lines=Project+Documentation;Cyber+Risk+Quantification+Explained;From+Raw+CVE+Data+to+Board+Room+Decisions)](https://git.io/typing-svg)

</div>

<div align="center">

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![CVSS](https://img.shields.io/badge/CVSS_Scoring-red?style=for-the-badge&logoColor=white)
![MITRE](https://img.shields.io/badge/MITRE_ATT%26CK-darkred?style=for-the-badge&logoColor=white)
![FAIR](https://img.shields.io/badge/FAIR_Model-orange?style=for-the-badge&logoColor=white)

</div>

---

## 1️⃣ Project Overview

**CyberPulse** answers the most important question every CISO and CFO asks:

> ***"How much is this cyber threat costing us — and where do we fix first?"***

This project ingests real CVE vulnerability data, applies a custom risk scoring engine inspired by MITRE ATT&CK, quantifies financial exposure using FAIR-style modeling, and delivers executive-level insights through a Power BI dashboard — bridging the gap between technical security data and business decision-making.

---

## 2️⃣ Business Problem

| Challenge | Impact |
|-----------|--------|
| 1,314+ vulnerabilities across infrastructure | No clear view of which to fix first |
| Technical CVSS scores not understood by leadership | Poor executive decision-making |
| No financial context attached to vulnerabilities | Security budget misallocation |
| Attack vectors not weighted by exploitability | Critical network threats treated same as local ones |
| No priority ranking for remediation | Security teams waste time on low-risk issues |

---

## 3️⃣ Data Source

The dataset uses **real CVE vulnerability data from the NVD (National Vulnerability Database)** — the official US government repository for vulnerability intelligence.

| Attribute | Details |
|-----------|---------|
| Total Records | 1,314 vulnerabilities |
| Source | NVD — National Vulnerability Database |
| Key Fields | CVE ID, CVSS Score, Attack Vector, Description, Affected OS |
| CVSS Score Range | 2.2 minimum to 10.0 maximum |
| Average CVSS Score | 6.79 |
| Framework Reference | MITRE ATT&CK, CVSS v3.1, FAIR Model |

---

## 4️⃣ Tools and Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.10** | Core ETL pipeline and risk modeling |
| **Pandas** | Data loading, cleaning, and transformation |
| **NumPy** | Numerical calculations and array operations |
| **Matplotlib** | Severity and attack vector charts |
| **Seaborn** | Enhanced chart styling |
| **Power BI** | Executive-grade dashboard and KPI visualization |
| **CVE / NVD Dataset** | Real vulnerability data source |
| **MITRE ATT&CK** | Threat intelligence framework reference |
| **FAIR Model** | Financial risk quantification inspiration |

---

## 5️⃣ How It Works

```
Raw CVE Vulnerability Data (NVD)
        │
        ▼
┌─────────────────────┐
│  Data Loading       │  — 1,314 CVE records loaded from NVD dataset
│  & Exploration      │  — Shape, columns, missing values, CVSS stats
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Severity           │  — CVSS score mapped to Critical/High/Medium/Low
│  Classification     │  — Official CVSS v3.1 severity rating scale
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Attack Vector      │  — CVSS string parsed to extract AV code
│  Extraction         │  — NETWORK / ADJACENT / LOCAL / PHYSICAL
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Risk Scoring       │  — Risk Score = CVSS Score x Attack Vector Weight
│  Engine             │  — Network = 1.0, Local = 0.5, Physical = 0.3
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Financial Impact   │  — FAIR-inspired dollar exposure per vulnerability
│  Model              │  — Critical = $500K, High = $150K, Medium = $50K
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Output                                 │
│  ├── Severity distribution chart        │
│  ├── Attack vector distribution chart   │
│  ├── Top 10 priority vulnerabilities    │
│  ├── cyber_risk_final.csv (Power BI)    │
│  └── Executive Power BI Dashboard       │
└─────────────────────────────────────────┘
```

---

## 6️⃣ Risk Scoring Engine — Core Logic

The heart of CyberPulse is the **custom risk scoring engine** — going beyond raw CVSS scores by weighting vulnerabilities based on how they can be exploited:

```python
def calculate_risk_score(row):
    vector_weights = {
        'NETWORK':  1.0,   # Remotely exploitable — most dangerous
        'ADJACENT': 0.7,   # Requires network proximity
        'LOCAL':    0.5,   # Requires local system access
        'PHYSICAL': 0.3    # Requires physical device access
    }
    weight = vector_weights.get(row['Attack Vector Clean'], 0.5)
    return round(row['CVSS Score'] * weight, 2)
```

**Why weight attack vectors?**
A NETWORK vulnerability affects every internet-connected device — far more dangerous than a LOCAL or PHYSICAL one that requires direct access. This weighting reflects real-world exploitability.

**Risk Score Results:**

| Metric | Value |
|--------|-------|
| Maximum Risk Score | 10.0 (Critical + Network) |
| Minimum Risk Score | 0.72 |
| Average Risk Score | 5.77 |

---

## 7️⃣ Severity Classification — CVSS v3.1 Scale

```python
def classify_severity(score):
    if score >= 9.0:  return 'Critical'   # Patch immediately
    elif score >= 7.0: return 'High'      # Patch within 30 days
    elif score >= 4.0: return 'Medium'    # Patch within 90 days
    else:              return 'Low'       # Patch when possible
```

**Severity Distribution Results:**

| Severity | Count | Recommended Action |
|----------|-------|--------------------|
| 🔴 Critical | 169 | Patch immediately |
| 🟠 High | 465 | Patch within 30 days |
| 🟡 Medium | 602 | Patch within 90 days |
| 🟢 Low | 78 | Patch when possible |

---

## 8️⃣ Financial Impact Model — FAIR Inspired

Translating every vulnerability into an estimated **dollar cost if exploited** — the language executives and boards actually understand:

```python
def estimate_financial_impact(cvss_score):
    if cvss_score >= 9.0:  return 500000  # Critical: $500K
    elif cvss_score >= 7.0: return 150000  # High: $150K
    elif cvss_score >= 4.0: return 50000   # Medium: $50K
    else:                   return 10000   # Low: $10K
```

**Financial Exposure Results:**

| Category | Exposure |
|----------|---------|
| **Total Financial Exposure** | $185,130,000 |
| Critical Vulnerability Exposure | $84,500,000 |
| High Vulnerability Exposure | $69,750,000 |
| Top 10 Combined Exposure | $5,000,000 |

---

## 9️⃣ Key Metrics and Results

| Metric | Value |
|--------|-------|
| **Total Vulnerabilities Analyzed** | 1,314 |
| **Average CVSS Risk Score** | 5.77 |
| **Total Financial Exposure** | $185,130,000 |
| **Critical Vulnerabilities** | 169 |
| **Network-Based Threats** | 893 (67.96%) |
| **Top 10 Combined Exposure** | $5,000,000 |
| **Manual Triage Time Reduced** | ~2-3 hours per assessment |

---

## 🔟 Attack Vector Distribution

| Attack Vector | Count | Percentage | Danger Level |
|---------------|-------|-----------|--------------|
| 🌐 NETWORK | 893 | 67.96% | Highest — remotely exploitable |
| 💻 LOCAL | 343 | 26.10% | Medium — requires local access |
| 📡 ADJACENT | 61 | 4.64% | Lower — requires network proximity |
| 🖐 PHYSICAL | 17 | 1.29% | Lowest — requires physical access |

**Key Finding:** Nearly 68% of all vulnerabilities are NETWORK-based — meaning they can be exploited remotely over the internet without any physical or local access.

---

## 1️⃣1️⃣ Top 10 Priority Vulnerabilities

All top 10 vulnerabilities share these characteristics:

| Attribute | Value |
|-----------|-------|
| Risk Score | 10.0 (maximum) |
| Attack Vector | NETWORK (remotely exploitable) |
| Financial Impact Each | $500,000 |
| Combined Top 10 Exposure | $5,000,000 |
| Recommended Action | Patch immediately |

---

## 1️⃣2️⃣ Dashboard Panels — Power BI

| Panel | What It Shows |
|-------|--------------|
| Total Vulnerabilities KPI | 1,314 vulnerabilities in scope |
| Average Risk Score KPI | 5.77 overall risk score |
| Financial Exposure KPI | $185M total estimated exposure |
| Severity Distribution Chart | Critical vs High vs Medium vs Low breakdown |
| Attack Vector Distribution | 67.96% Network-based threats highlighted |
| Top Priority Vulnerabilities | Ranked by risk score for immediate action |

---

## 1️⃣3️⃣ Skills Demonstrated

`Cyber Risk Quantification` · `CVSS v3.1 Scoring` · `MITRE ATT&CK Framework` · `FAIR Financial Modeling` · `Power BI Dashboard` · `Python ETL Pipeline` · `Pandas` · `Attack Vector Analysis` · `Executive Reporting` · `Vulnerability Prioritization` · `Data Engineering` · `Security Analytics`

---

## 🚀 Future Roadmap

- [ ] Integrate live CVE feed via NVD API for real-time data
- [ ] Add MITRE ATT&CK technique mapping per vulnerability
- [ ] Build ML model to predict future high-risk CVEs
- [ ] Deploy as real-time web dashboard
- [ ] Add remediation cost vs risk reduction ROI calculator

---

## ⚙️ How to Run

### Option 1 — Jupyter Notebook (Recommended)
```bash
jupyter notebook notebooks/cyber_risk_analysis.ipynb
```

### Option 2 — Python Script
```bash
python cyber_risk_analysis.py
```

### Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

---

## 👤 Author

**Reshma Keshireddy** — Cybersecurity & Data Analytics

LinkedIn: https://linkedin.com/in/reshma-keshireddy-1283b91b6
GitHub: https://github.com/reshmakeshireddy1021-bit

---

> *"Good security analytics doesn't just find risk — it helps leadership understand what that risk costs."*

---

> *This project is for educational and portfolio purposes only.*
