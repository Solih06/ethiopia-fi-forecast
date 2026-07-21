import os
import pandas as pd
from typing import Tuple

class DataLoader:
    """Utility class to load and validate unified financial inclusion datasets."""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        self.unified_path = os.path.join(data_dir, "ethiopia_fi_unified_data.csv")
        self.ref_path = os.path.join(data_dir, "reference_codes.csv")

    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Loads raw unified dataset and reference codes."""
        if not os.path.exists(self.unified_path):
            raise FileNotFoundError(f"Unified dataset not found at {self.unified_path}")
        
        df_unified = pd.read_csv(self.unified_path)
        df_ref = pd.read_csv(self.ref_path) if os.path.exists(self.ref_path) else pd.DataFrame()
        return df_unified, df_ref

    def get_parsed_records(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Splits unified dataset into observations, events, impact links, and targets."""
        df_unified, _ = self.load_raw_data()
        
        obs = df_unified[df_unified['record_type'] == 'observation'].copy()
        events = df_unified[df_unified['record_type'] == 'event'].copy()
        impacts = df_unified[df_unified['record_type'] == 'impact_link'].copy()
        targets = df_unified[df_unified['record_type'] == 'target'].copy()
        
        return obs, events, impacts, targets