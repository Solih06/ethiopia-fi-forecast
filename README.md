
# Forecasting Financial Inclusion in Ethiopia

An event-augmented time-series forecasting system designed to track, model, and analyze Ethiopia's digital financial transformation. This system bridges the gap between highly sparse demand-side survey data (World Bank Global Findex) and high-frequency supply-side administrative indicators (National Bank of Ethiopia, EthSwitch) to project core inclusion metrics through 2027.

## 📊 Core Data Framework (Unified Schema)

The architecture utilizes a unified relational data schema where observations, historical events, policy targets, and cross-indicator linkages share a standardized column format. This structurally removes pillar assignment biases and models downstream indicator shocks dynamically.

### Dataset Composition (Post-Enrichment)

| Record Type | Count | Core Pillars Covered | Primary Purpose |
| :--- | :---: | :--- | :--- |
| `observation` | 34 | `access`, `usage`, `infrastructure` | Tracks actual measured historical percentages, transaction volumes, and enabler densities. |
| `event` | 11 | *Left blank intentionally* | Anchors policy changes, product rollouts (Telebirr, M-Pesa), and structural shocks. |
| `impact_link` | 15 | `access`, `usage` | Maps specific event shocks to related indicators using comparable market evidence. |
| `target` | 3 | `access` | Represents official national development goals (e.g., NFIS-II targets). |

---

## 📈 Exploratory Analysis & Key Trends

### 1. Historical Account Ownership Trajectory (Access)
The demand-side survey records highlight a critical structural inflection point:

```text
  Account Ownership Rate (%)
  100 |
   80 |
   60 |                                         [2024: 49%] -> Stagnation Phase
   40 |                          [2021: 46%] -------o
   20 |           [2014: 22%] ------o
    0 [2011: 14%] ------o
      +-----------+-----------+-----------+-----------+
      2011        2014        2017        2021        2024
  ```
**The Deceleration Paradox** : While mobile wallets exploded to over 65 million combined users between 2021 and 2024, unique account ownership grew by only +3 percentage points. This highlights a sharp divide between total account registrations and actual unique ownership.
2. Digital Transactions (Usage Shift)The P2P-ATM Crossover: Interoperable peer-to-peer (P2P) transfers have officially surpassed physical ATM cash withdrawals across the EthSwitch clearing network.  Ecosystem Nuance: Unlike early peer markets, Ethiopia's digital wallets are heavily utilized directly for retail commerce transactions rather than standard domestic transfers alone.  

## 📂 Project Architecture
```text
ethiopia-fi-forecast/
├── data/
│   ├── raw/                      # Baseline and enriched datasets
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/                # Model-ready historical intervals
├── src/                          # Modular production scripts
│   ├── __init__.py
│   ├── data_loader.py            # Unified schema parser and filtering tools
│   ├── enrich_dataset.py         # Task 1 dataset enrichment pipeline
│   └── run_eda.py                # Task 2 analysis and visualization engine
├── notebooks/
│   └── 01_exploratory_data_analysis.ipynb
├── reports/
│   └── figures/                  # Output analysis charts (PNG formats)
│       ├── 01_account_ownership_trajectory.png
│       └── 02_temporal_coverage_profile.png
├── data_enrichment_log.md        # Audit tracking for added indicators
├── requirements.txt              # Project dependency manifest
└── README.md                     # Documentation entry point
```
## ⚙️ Local Environment & Execution Setup
Ensure your local Python environment is activated before running the automation layer
1. Initialize Virtual Environment & Install Tools
```bash
# Create environment
python -m venv .venv

# Activate environment
.venv\Scripts\Activate.ps1

# Install core dependencies
pip install -r requirements.txt
```
2. Execute the Data Enrichment Pipeline (Task 1)
Appends disaggregated Findex microdata rows, infrastructure enabler records, and policy milestones to your raw storage
```bash
python src/enrich_dataset.py
```
3. Generate Analytical Visualizations (Task 2)
Processes the sparse data tracks and exports diagnostic figures directly into reports/figures/
```bash
python src/run_eda.py
```
## 📑 Next Development Milestones
Task 3: Build the quantitative Event-Indicator Matrix to estimate shock weights and lag matrices using domestic and regional markers[cite: 1].

Task 4: Deploy event-augmented regression models to project Access and Usage outcomes across base, optimistic, and pessimistic scenarios for 2025–2027[cite: 1].

Task 5: Build and run the Streamlit interactive dashboard (dashboard/app.py)
