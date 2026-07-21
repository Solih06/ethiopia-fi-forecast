import os
import pandas as pd
import numpy as np
from typing import Dict, Tuple

class EventImpactModel:
    """Builds Association Matrix and calculates event impact multipliers for indicators."""

    def __init__(self, events_df: pd.DataFrame, impact_links_df: pd.DataFrame):
        self.events_df = events_df.copy()
        self.impact_links_df = impact_links_df.copy()
        self._preprocess()

    def _preprocess(self):
        """Ensures proper date parsing and numeric types."""
        self.events_df['event_date'] = pd.to_datetime(self.events_df['observation_date'])
        self.impact_links_df['impact_magnitude'] = pd.to_numeric(
            self.impact_links_df['value_numeric'], errors='coerce'
        ).fillna(0.0)
        self.impact_links_df['lag_months'] = pd.to_numeric(
            self.impact_links_df['lag_months'], errors='coerce'
        ).fillna(0.0)

    def build_association_matrix(self) -> pd.DataFrame:
        """Translates impact links into an Event-Indicator Association Matrix.
        
        Rows: Events
        Columns: Target Indicators (e.g., ACC_OWNERSHIP, ACC_MM_ACCOUNT, USG_DIGITAL_PAYMENT)
        Values: Signed Impact Magnitude (+/- percentage points)
        """
        merged = pd.merge(
            self.impact_links_df,
            self.events_df[['id', 'name', 'event_date']],
            left_on='parent_id',
            right_on='id',
            how='left'
        )
        
        # Calculate signed numeric impact magnitude based on impact_direction
        merged['signed_magnitude'] = merged.apply(
            lambda row: row['impact_magnitude'] if str(row.get('impact_direction', 'positive')).lower() == 'positive' else -row['impact_magnitude'],
            axis=1
        )
        
        matrix = merged.pivot_table(
            index='name',
            columns='related_indicator',
            values='signed_magnitude',
            aggfunc='sum',
            fill_value=0.0
        )
        return matrix

    def calculate_cumulative_event_effect(self, indicator_code: str, target_year: int) -> float:
        """Calculates time-lagged, cumulative event effects for a specific target forecast year."""
        merged = pd.merge(
            self.impact_links_df[self.impact_links_df['related_indicator'] == indicator_code],
            self.events_df[['id', 'name', 'event_date']],
            left_on='parent_id',
            right_on='id'
        )
        
        total_effect = 0.0
        for _, row in merged.iterrows():
            event_year = row['event_date'].year + (row['event_date'].month / 12.0)
            lag_years = row['lag_months'] / 12.0
            effective_year = event_year + lag_years
            
            # If target year has reached or passed the effective date, apply intervention shock
            if target_year >= effective_year:
                direction = 1.0 if str(row.get('impact_direction', 'positive')).lower() == 'positive' else -1.0
                total_effect += row['impact_magnitude'] * direction
                
        return total_effect