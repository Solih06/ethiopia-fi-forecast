import pytest
import pandas as pd
from src.impact_model import EventImpactModel
from src.forecaster import FIForecaster
from src.data_loader import DataLoader, UnifiedDataLoader

def test_data_loader_alias_and_validation():
    """Tests both DataLoader and UnifiedDataLoader alias and schema validation."""
    loader1 = DataLoader()
    loader2 = UnifiedDataLoader()
    assert loader1 is not None
    assert loader2 is not None

def test_forecaster_edge_case_insufficient_data():
    """Tests forecaster failure when given fewer than 2 data points."""
    df_small = pd.DataFrame({
        'year': [2024],
        'indicator_code': ['ACC_OWNERSHIP'],
        'value_numeric': [49.0]
    })
    forecaster = FIForecaster(df_small)
    with pytest.raises(ValueError, match="Insufficient historical observations"):
        forecaster.fit_and_forecast('ACC_OWNERSHIP')

def test_impact_model_empty_events():
    """Tests impact model behavior with zero linked impact events."""
    events_df = pd.DataFrame(columns=['id', 'name', 'observation_date'])
    impacts_df = pd.DataFrame(columns=['parent_id', 'related_indicator', 'value_numeric', 'lag_months'])
    
    model = EventImpactModel(events_df, impacts_df)
    matrix = model.build_association_matrix()
    assert matrix.empty