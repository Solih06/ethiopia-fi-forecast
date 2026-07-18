import os
import pandas as pd

class UnifiedDataLoader:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        self.unified_path = os.path.join(data_dir, "ethiopia_fi_unified_data.csv")
        self.reference_path = os.path.join(data_dir, "reference_codes.csv")

    def load_raw_data(self):
        """Loads the baseline unified dataset."""
        if not os.path.exists(self.unified_path):
            raise FileNotFoundError(f"Unified dataset not found at {self.unified_path}. Please place the starter file there.")
        
        df = pd.read_csv(self.unified_path)
        # Ensure date columns are formatted correctly
        if 'observation_date' in df.columns:
            df['observation_date'] = pd.to_datetime(df['observation_date'])
        return df

    def split_by_record_type(self, df):
        """Splits the single schema dataframe into semantic data subsets."""
        observations = df[df['record_type'] == 'observation'].copy()
        events = df[df['record_type'] == 'event'].copy()
        impact_links = df[df['record_type'] == 'impact_link'].copy()
        targets = df[df['record_type'] == 'target'].copy()
        
        return observations, events, impact_links, targets

    def get_indicator_subset(self, observations_df, indicator_code):
        """Helper to pull out specific time-series lines cleanly."""
        subset = observations_df[observations_df['indicator_code'] == indicator_code].copy()
        return subset.sort_values(by='observation_date')