# =============================================================================
# CyberPulse: Cyber Risk Quantification Dashboard
# Author: Reshma Keshireddy
# Description: Ingests real CVE vulnerability data, applies a custom risk
#              scoring engine inspired by MITRE ATT&CK, quantifies financial
#              exposure using FAIR-style modeling, and exports a clean dataset
#              for executive-level Power BI dashboard visualization.
# Stack: Python | Pandas | NumPy | Matplotlib | Seaborn | Power BI
# =============================================================================

# =============================================================================
# STEP 1 — Import Libraries
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

print("=" * 60)
print("CyberPulse: Cyber Risk Quantification Dashboard")
print("=" * 60)
print("Libraries loaded successfully")
print(f"Run timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# =============================================================================
# STEP 2 — Load Dataset
# =============================================================================
# Update this path to match your local folder structure
DATA_PATH = r"Data\Raw\nvd_vulnerabilities_with_os.csv"

df = pd.read_csv(DATA_PATH)

print(f"\nDataset loaded: {df.shape[0]} records, {df.shape[1]} columns")
print(f"Columns: {df.columns.tolist()}")
print("\nSample data (first 5 rows):")
print(df.head())


# =============================================================================
# STEP 3 — Explore Dataset
# =============================================================================
print("\n" + "=" * 60)
print("DATASET EXPLORATION")
print("=" * 60)
print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nCVSS Score Statistics:")
print(df["CVSS Score"].describe())


# =============================================================================
# STEP 4 — Severity Classification (CVSS v3.1 Official Scale)
# =============================================================================
def classify_severity(score):
    """
    Maps CVSS numerical scores to official CVSS v3.1 severity labels.

    Scale:
        Critical : CVSS >= 9.0  — patch immediately
        High     : CVSS >= 7.0  — patch within 30 days
        Medium   : CVSS >= 4.0  — patch within 90 days
        Low      : CVSS <  4.0  — patch when possible

    Args:
        score (float): CVSS score between 0 and 10

    Returns:
        str: Severity label
    """
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"


df["Severity Level"] = df["CVSS Score"].apply(classify_severity)

print("\n" + "=" * 60)
print("SEVERITY DISTRIBUTION")
print("=" * 60)
print(df["Severity Level"].value_counts())


# =============================================================================
# STEP 5 — Severity Distribution Chart
# =============================================================================
os.makedirs("screenshots", exist_ok=True)

plt.figure(figsize=(8, 5))
severity_order = ["Critical", "High", "Medium", "Low"]
colors = ["#d32f2f", "#f57c00", "#fbc02d", "#388e3c"]

df["Severity Level"].value_counts().reindex(severity_order).plot(
    kind="bar", color=colors, edgecolor="black"
)

plt.title("Vulnerability Severity Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Severity Level")
plt.ylabel("Number of Vulnerabilities")
plt.xticks(rotation=0)

for i, v in enumerate(df["Severity Level"].value_counts().reindex(severity_order)):
    plt.text(i, v + 5, str(v), ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("screenshots/severity_distribution.png", dpi=150)
plt.show()
print("Severity chart saved to screenshots/severity_distribution.png")


# =============================================================================
# STEP 6 — Extract Attack Vector from CVSS String
# =============================================================================
def extract_attack_vector(cvss_string):
    """
    Parses the raw CVSS vector string to extract the Attack Vector code.

    CVSS v3.1 Attack Vector codes:
        AV:N = NETWORK   — remotely exploitable (most dangerous)
        AV:A = ADJACENT  — requires same network
        AV:L = LOCAL     — requires local system access
        AV:P = PHYSICAL  — requires physical device access

    Args:
        cvss_string (str): Full CVSS vector string e.g. CVSS:3.1/AV:N/AC:L/...

    Returns:
        str: Human-readable attack vector label
    """
    try:
        parts = str(cvss_string).split("/")
        for part in parts:
            if part.startswith("AV:"):
                av = part.split(":")[1]
                mapping = {
                    "N": "NETWORK",
                    "A": "ADJACENT",
                    "L": "LOCAL",
                    "P": "PHYSICAL"
                }
                return mapping.get(av, "UNKNOWN")
    except:
        return "UNKNOWN"
    return "UNKNOWN"


df["Attack Vector Clean"] = df["Attack Vector"].apply(extract_attack_vector)

print("\n" + "=" * 60)
print("ATTACK VECTOR DISTRIBUTION")
print("=" * 60)
print(df["Attack Vector Clean"].value_counts())
print("\nAttack Vector Percentage:")
print(df["Attack Vector Clean"].value_counts(normalize=True).mul(100).round(2))


# =============================================================================
# STEP 7 — Attack Vector Distribution Chart
# =============================================================================
plt.figure(figsize=(8, 5))
colors = ["#d32f2f", "#f57c00", "#fbc02d", "#388e3c"]

df["Attack Vector Clean"].value_counts().plot(
    kind="bar", color=colors, edgecolor="black"
)

plt.title("Vulnerability Attack Vector Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Attack Vector")
plt.ylabel("Number of Vulnerabilities")
plt.xticks(rotation=0)

for i, v in enumerate(df["Attack Vector Clean"].value_counts()):
    plt.text(i, v + 5, str(v), ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("screenshots/attack_vector_distribution.png", dpi=150)
plt.show()
print("Attack vector chart saved to screenshots/attack_vector_distribution.png")


# =============================================================================
# STEP 8 — Risk Scoring Engine
# =============================================================================
def calculate_risk_score(row):
    """
    Calculates a custom risk score by weighting CVSS scores based on
    attack vector exploitability — inspired by MITRE ATT&CK framework.

    Risk Formula:
        Risk Score = CVSS Score x Attack Vector Weight

    Attack Vector Weights:
        NETWORK  : 1.0 — full weight, remotely exploitable
        ADJACENT : 0.7 — reduced weight, requires network proximity
        LOCAL    : 0.5 — half weight, requires local access
        PHYSICAL : 0.3 — lowest weight, requires physical access

    Args:
        row (pd.Series): DataFrame row with CVSS Score and Attack Vector

    Returns:
        float: Weighted risk score
    """
    vector_weights = {
        "NETWORK":  1.0,
        "ADJACENT": 0.7,
        "LOCAL":    0.5,
        "PHYSICAL": 0.3
    }
    weight = vector_weights.get(str(row["Attack Vector Clean"]).upper(), 0.5)
    return round(row["CVSS Score"] * weight, 2)


df["Risk Score"] = df.apply(calculate_risk_score, axis=1)

print("\n" + "=" * 60)
print("RISK SCORING RESULTS")
print("=" * 60)
print(f"Maximum Risk Score  : {df['Risk Score'].max()}")
print(f"Minimum Risk Score  : {df['Risk Score'].min()}")
print(f"Average Risk Score  : {df['Risk Score'].mean().round(2)}")
print("\nTop 10 Highest Risk IPs:")
print(df[["CVE ID", "CVSS Score", "Attack Vector Clean", "Risk Score"]]
      .sort_values("Risk Score", ascending=False)
      .head(10)
      .to_string(index=False))


# =============================================================================
# STEP 9 — Financial Impact Model (FAIR-Inspired)
# =============================================================================
def estimate_financial_impact(cvss_score):
    """
    Estimates the dollar exposure per vulnerability if exploited.
    Inspired by the FAIR (Factor Analysis of Information Risk) model.

    Financial Impact Scale:
        Critical (>= 9.0) : $500,000  — major breach, fines, reputational damage
        High     (>= 7.0) : $150,000  — significant incident, recovery costs
        Medium   (>= 4.0) : $50,000   — moderate incident, patching costs
        Low      (<  4.0) : $10,000   — minor incident, minimal impact

    Args:
        cvss_score (float): CVSS score between 0 and 10

    Returns:
        int: Estimated dollar exposure
    """
    if cvss_score >= 9.0:
        return 500000
    elif cvss_score >= 7.0:
        return 150000
    elif cvss_score >= 4.0:
        return 50000
    else:
        return 10000


df["Financial Impact ($)"] = df["CVSS Score"].apply(estimate_financial_impact)

total_exposure   = df["Financial Impact ($)"].sum()
critical_exposure = df[df["CVSS Score"] >= 9.0]["Financial Impact ($)"].sum()
high_exposure    = df[(df["CVSS Score"] >= 7.0) & (df["CVSS Score"] < 9.0)]["Financial Impact ($)"].sum()

print("\n" + "=" * 60)
print("FINANCIAL EXPOSURE SUMMARY")
print("=" * 60)
print(f"Total Financial Exposure      : ${total_exposure:,}")
print(f"Critical Vulnerability Exposure: ${critical_exposure:,}")
print(f"High Vulnerability Exposure    : ${high_exposure:,}")
print(f"Total Vulnerabilities Scored   : {len(df)}")


# =============================================================================
# STEP 10 — Top 10 Priority Vulnerabilities
# =============================================================================
top_10 = df.sort_values(by="Risk Score", ascending=False).head(10)

print("\n" + "=" * 70)
print("TOP 10 HIGHEST PRIORITY VULNERABILITIES")
print("=" * 70)
print(top_10[[
    "CVE ID", "CVSS Score", "Attack Vector Clean",
    "Risk Score", "Financial Impact ($)"
]].to_string(index=False))
print("=" * 70)
print(f"Combined Top 10 Exposure: ${top_10['Financial Impact ($)'].sum():,}")


# =============================================================================
# STEP 11 — Export Clean Dataset for Power BI
# =============================================================================
os.makedirs("Data/Processed", exist_ok=True)

df_export = df[[
    "CVE ID", "Description", "CVSS Score",
    "Attack Vector Clean", "Risk Score",
    "Financial Impact ($)", "Severity Level"
]].copy()

df_export.to_csv("Data/Processed/cyber_risk_final.csv", index=False)

print("\n" + "=" * 60)
print("CYBERPULSE PIPELINE COMPLETE")
print("=" * 60)
print(f"Dataset exported     : Data/Processed/cyber_risk_final.csv")
print(f"Total records        : {len(df_export)}")
print(f"Total Exposure       : ${total_exposure:,}")
print(f"Critical Count       : {len(df[df['Severity Level'] == 'Critical'])}")
print(f"Network Threats      : {len(df[df['Attack Vector Clean'] == 'NETWORK'])}")
print(f"Average Risk Score   : {df['Risk Score'].mean().round(2)}")
print("\nLoad Data/Processed/cyber_risk_final.csv into Power BI to build the dashboard.")
print("=" * 60)
