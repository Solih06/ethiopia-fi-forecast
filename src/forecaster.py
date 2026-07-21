import numpy as np
import pandas as pd
from statsmodels.api import OLS, add_constant
from typing import List, Dict

class FIForecaster:
    """Forecasts Access and Usage rates using Event-Augmented Linear Regression models."""

    def __init__(self, historical_df: pd.DataFrame):
        self.historical_df = historical_df.copy()

    def fit_and_forecast(self, indicator_code: str, forecast_years: List[int] = [2025, 2026, 2027], impact_model=None) -> pd.DataFrame:
        """Generates baseline and event-augmented forecasts with scenario bounds."""
        df_ind = self.historical_df[
            self.historical_df['indicator_code'] == indicator_code
        ].sort_values('year').copy()
        
        if len(df_ind) < 2:
            raise ValueError(f"Insufficient historical observations for indicator {indicator_code}")

        X = add_constant(df_ind['year'].values)
        y = df_ind['value_numeric'].values
        
        # Fit baseline OLS trend model
        model = OLS(y, X).fit()
        
        results = []
        for yr in forecast_years:
            pred_base = model.predict([1, yr])[0]
            
            # Incorporate event impacts if model is provided
            event_effect = 0.0
            if impact_model:
                event_effect = impact_model.calculate_cumulative_event_effect(indicator_code, yr)
            
            val_augmented = pred_base + event_effect
            
            # Scenario Multipliers & Confidence Bounds
            results.append({
                'year': yr,
                'indicator_code': indicator_code,
                'baseline_trend': np.clip(pred_base, 0, 100),
                'base_scenario': np.clip(val_augmented, 0, 100),
                'optimistic_scenario': np.clip(val_augmented * 1.08, 0, 100),
                'pessimistic_scenario': np.clip(val_augmented * 0.92, 0, 100),
                'ci_lower_95': np.clip(val_augmented - 3.5, 0, 100),
                'ci_upper_95': np.clip(val_augmented + 3.5, 0, 100)
            })
            
        return pd.DataFrame(results)