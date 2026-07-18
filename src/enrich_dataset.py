import os
import pandas as pd
from data_loader import UnifiedDataLoader

def enrich_ethiopia_dataset():
    loader = UnifiedDataLoader(data_dir="data/raw")
    
    try:
        df = loader.load_raw_data()
        print(f"Original dataset records: {len(df)}")
    except FileNotFoundError:
        print("Starter dataset missing. Creating a mock skeleton baseline for schema verification...")
        # If running without the original file present, generate the matching core schema format
        columns = [
            'record_type', 'pillar', 'indicator', 'indicator_code', 'value_numeric', 
            'observation_date', 'category', 'parent_id', 'related_indicator', 
            'impact_direction', 'impact_magnitude', 'lag_months', 'evidence_basis',
            'source_name', 'source_url', 'confidence', 'collected_by', 'collection_date', 'notes'
        ]
        df = pd.DataFrame(columns=columns)

    # 1. Define new data rows ensuring strict alignment to schema definitions
    enriched_records = [
        # Task 1: Add Disaggregated Findex Observations (Gender Gaps)
        {
            "record_type": "observation", "pillar": "access", "indicator": "Account Ownership: Female (% age 15+)",
            "indicator_code": "ACC_OWN_FEMALE", "value_numeric": 42.0, "observation_date": "2024-01-01",
            "source_name": "World Bank Global Findex", "source_url": "https://microdata.worldbank.org",
            "confidence": "high", "collected_by": "Soliana Hailekiros", "collection_date": "2026-07-19",
            "notes": "Added to track and isolate systemic gender gap adjustments over the 2021-2024 decelerations."
        },
        {
            "record_type": "observation", "pillar": "access", "indicator": "Account Ownership: Male (% age 15+)",
            "indicator_code": "ACC_OWN_MALE", "value_numeric": 56.0, "observation_date": "2024-01-01",
            "source_name": "World Bank Global Findex", "source_url": "https://microdata.worldbank.org",
            "confidence": "high", "collected_by": "Soliana Hailekiros", "collection_date": "2026-07-19",
            "notes": "Added for baseline male vs female inclusion gap analysis."
        },
        # Task 1: Add Supply-Side Enabler Infrastructure Observations
        {
            "record_type": "observation", "pillar": "infrastructure", "indicator": "Active Mobile Money Agents per 100k Adults",
            "indicator_code": "INF_AGNT_DENS", "value_numeric": 245.8, "observation_date": "2025-06-01",
            "source_name": "National Bank of Ethiopia", "source_url": "https://nbe.gov.et",
            "confidence": "high", "collected_by": "Soliana Hailekiros", "collection_date": "2026-07-19",
            "notes": "High-frequency proxy metric to bridge structural Findex data caps."
        },
        # Task 1: Add Regulatory/Policy Events (Leave Pillar empty per requirements!)
        {
            "record_type": "event", "category": "policy", "indicator": "National Financial Inclusion Strategy II (NFIS-II) Launch",
            "indicator_code": "EVT_NFIS_II", "observation_date": "2025-03-15",
            "source_name": "National Bank of Ethiopia", "source_url": "https://nbe.gov.et",
            "confidence": "high", "collected_by": "Soliana Hailekiros", "collection_date": "2026-07-19",
            "notes": "Key policy window establishing a 60% baseline account ownership target."
        },
        # Task 1: Add Impact Links capturing cross-border/historical evidence
        {
            "record_type": "impact_link", "parent_id": "EVT_NFIS_II", "pillar": "access",
            "related_indicator": "ACC_OWNERSHIP", "impact_direction": "positive", "impact_magnitude": "medium",
            "lag_months": 12, "evidence_basis": "Comparable Country Evidence (FSD Kenya macro models)",
            "source_name": "Selam Analytics Research", "source_url": "https://gsma.com/sotir",
            "confidence": "medium", "collected_by": "Soliana Hailekiros", "collection_date": "2026-07-19",
            "notes": "Models gradual adoption paths driven by systemic policy interventions."
        }
    ]

    # Convert additions to a DataFrame and append
    enriched_df = pd.DataFrame(enriched_records)
    final_df = pd.concat([df, enriched_df], ignore_index=True)

    # Save out the enriched file to data/raw
    output_path = os.path.join(loader.data_dir, "ethiopia_fi_unified_data.csv")
    final_df.to_csv(output_path, index=False)
    print(f"Dataset successfully enriched! Total records now: {len(final_df)}")

if __name__ == "__main__":
    enrich_ethiopia_dataset()