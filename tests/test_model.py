import pytest
import pandas as pd
from src.impact_model import EventImpactModel
from src.forecaster import FIForecaster

def test_event_impact_model_matrix():
    # Sample Mock Data for Events and Impact Links
    events_df = pd.DataFrame({
        'id': ['EVT_01'],
        'name': ['Telebirr Launch'],
        'observation_date': ['2021-05-01']
    })
    
    impact_links_df = pd.DataFrame({
        'parent_id': ['EVT_01'],
        'related_indicator': ['ACC_MM_ACCOUNT'],
        'value_numeric': [4.5],
        'impact_direction': ['positive'],
        'lag_months': [0]
    })
    
    model = EventImpactModel(events_df, impact_links_df)
    matrix = model.build_association_matrix()
    
    assert not matrix.empty
    assert 'ACC_MM_ACCOUNT' in matrix.columns
    assert matrix.loc['Telebirr Launch', 'ACC_MM_ACCOUNT'] == 4.5

def test_forecaster_output():
    # Sample Mock Data for Historical Findex Indicators
    df_hist = pd.DataFrame({
        'year': [2011, 2014, 2017, 2021, 2024],
        'indicator_code': ['ACC_OWNERSHIP'] * 5,
        'value_numeric': [14.0, 22.0, 35.0, 46.0, 49.0]
    })
    
    forecaster = FIForecaster(df_hist)
    results = forecaster.fit_and_forecast('ACC_OWNERSHIP', forecast_years=[2025, 2026, 2027])
    
    assert len(results) == 3
    assert 'base_scenario' in results.columns
    assert results['base_scenario'].iloc[0] > 49.0  # Forecast for 2025 should exceed 2024 baseline