import os
import pandas as pd
from typing import Tuple, Optional
from src.config import UNIFIED_DATA_PATH, REF_CODES_PATH, REQUIRED_COLUMNS, VALID_RECORD_TYPES

class DataLoader:
    """Loads, validates, and parses unified financial inclusion data."""

    def __init__(self, data_dir: Optional[str] = None):
        self.unified_path = os.path.join(data_dir, "ethiopia_fi_unified_data.csv") if data_dir else UNIFIED_DATA_PATH
        self.ref_path = os.path.join(data_dir, "reference_codes.csv") if data_dir else REF_CODES_PATH

    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if not os.path.exists(self.unified_path):
            raise FileNotFoundError(f"Dataset missing at {self.unified_path}")
        
        df_unified = pd.read_csv(self.unified_path)
        self.validate_schema(df_unified)
        
        df_ref = pd.read_csv(self.ref_path) if os.path.exists(self.ref_path) else pd.DataFrame()
        return df_unified, df_ref

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Validates that required schema columns and record types are present."""
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Schema validation failed. Missing columns: {missing}")
        
        present_types = set(df['record_type'].dropna().unique())
        invalid_types = present_types - VALID_RECORD_TYPES
        if invalid_types:
            raise ValueError(f"Schema validation failed. Invalid record_types found: {invalid_types}")
        return True

    def get_parsed_records(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        df_unified, _ = self.load_raw_data()
        
        obs = df_unified[df_unified['record_type'] == 'observation'].copy()
        events = df_unified[df_unified['record_type'] == 'event'].copy()
        impacts = df_unified[df_unified['record_type'] == 'impact_link'].copy()
        targets = df_unified[df_unified['record_type'] == 'target'].copy()
        
        return obs, events, impacts, targets

# Class Alias to fix naming mismatches
UnifiedDataLoader = DataLoader