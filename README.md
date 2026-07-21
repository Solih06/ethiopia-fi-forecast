## Forecasting Financial Inclusion in Ethiopia (2025–2027)
An event-augmented time-series forecasting system designed to track, model, and analyze Ethiopia's digital financial transformation. This system bridges the gap between highly sparse demand-side survey data (World Bank Global Findex) and high-frequency supply-side administrative indicators (National Bank of Ethiopia, EthSwitch) to project core inclusion metrics through 2027.

## 📊 Core Data Framework (Unified Schema)
The architecture utilizes a unified relational data schema where observations, historical events, policy targets, and cross-indicator linkages share a standardized column format. This structurally removes pillar assignment biases and dynamically models downstream indicator shocks.

| Record Type | Count | Core Pillars Covered | Primary Purpose |
| :--- | :---: | :--- | :--- |
| **`observation`** | 34 | `access`, `usage`, `infrastructure` | Tracks actual measured historical percentages, transaction volumes, and enabler densities. |
| **`event`** | 11 | *Left blank intentionally* | Anchors policy changes, product rollouts (Telebirr, M-Pesa), and structural shocks. |
| **`impact_link`** | 15 | `access`, `usage` | Maps specific event shocks to related indicators using comparable market evidence. |
| **`target`** | 3 | `access` | Represents official national development goals (e.g., NFIS-II targets). |

## 📈 Exploratory Analysis & Key Findings
1. Historical Account Ownership Trajectory (Access)
Demand-side survey records highlight a critical structural inflection point:

Account Ownership Rate (%)
 100 |
  80 |
  60 |                                         [2024: 49%] -> Stagnation Phase
  40 |                           [2021: 46%] -------o
  20 |           [2014: 22%] ------o
   0 [2011: 14%] ------o
     +-----------+-----------+-----------+-----------+
      2011        2014        2017        2021        2024

**The Deceleration Paradox:** While mobile money registered wallets exploded to over 65 million users between 2021 and 2024, unique account ownership grew by only +3 percentage points (46% to 49%). This highlights a sharp divide between total account registrations (often multi-SIM/wallet holdings) and actual unique adult account ownership.

2. Digital Transactions (Usage Shift)
The P2P-ATM Crossover: Interoperable peer-to-peer (P2P) transfers across the EthSwitch network have officially surpassed physical ATM cash withdrawals in clearing volume.

Ecosystem Nuance: Unlike early peer market models, Ethiopia's mobile wallets are increasingly used directly for retail merchant payments and utility services.

## 📂 Repository Architecture
```text
ethiopia-fi-forecast/
├── .github/
│   └── workflows/
│       └── unittests.yml               # Automated CI/CD PyTest action
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.csv# Unified relational dataset
│   │   └── reference_codes.csv         # Indicator/Event reference mappings
│   └── processed/                      # Transformed modeling data
├── notebooks/
│   ├── 01_data_exploration_and_enrichment.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_event_impact_modeling.ipynb
│   └── 04_forecasting_access_and_usage.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py                  # Dataset parsing & verification
│   ├── impact_model.py                 # Task 3: Event-Indicator Association Matrix & impact calculations
│   └── forecaster.py                   # Task 4: Event-Augmented regression forecaster
├── dashboard/
│   └── app.py                          # Task 5: Interactive multi-page Streamlit dashboard
├── tests/
│   ├── __init__.py
│   ├── test_data.py                    # Unit tests for data loading pipelines
│   └── test_model.py                   # Unit tests for forecasting engines
├── reports/
│   └── figures/                        # Diagnostic plots and chart exports
├── data_enrichment_log.md              # Enriched schema change logs
├── requirements.txt                    # Dependency manifest
└── README.md                           # Documentation entry point
```

## ⚙️ Quickstart Guide
1. Environment Setup & Dependency Installation
Run the following commands in your terminal (PowerShell on Windows):
```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install required packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. Run Automated Unit Testing Suite
To test the data processing, event matrix calculations, and model predictions locally:
```bash
python -m pytest tests/ -v
```
3. Launch the Interactive Dashboard (Task 5)
Launch the multi-page Streamlit web app locally:
```bash
python -m streamlit run dashboard/app.py
```
Access the dashboard in your web browser at http://localhost:8501.

## 📑 Completed Development Milestones
**Task 1: Data Enrichment:** Built the unified relational dataset by joining Global Findex microdata, high-frequency clearing data from EthSwitch, macro proxy series, and peer market benchmarks.
**Task 2: Exploratory Data Analysis:** Modeled historical trends, investigated the 2021–2024 Access deceleration paradox, and documented the P2P-ATM transaction volume crossover.
**Task 3: Event Impact Modeling:** Built the EventImpactModel class to quantify policy/product intervention shocks (Telebirr, M-Pesa, Fayda Digital ID, EthSwitch mandate) into an Event-Indicator Association Matrix.
**Task 4: Forecasting Access & Usage (2025–2027):** Deployed an event-augmented linear regression forecasting engine with Base, Optimistic, and Pessimistic scenario trajectories.
**Task 5: Interactive Streamlit Dashboard:** Engineered a responsive web application featuring executive KPI summaries, historical trend analyses, heatmaps of event impact matrices, and downloadable forecast data.


