import pytest
import pandas as pd
import numpy as np
from src.config import ForecastConfig, ScenarioConfig, NFIS_TARGET_2027

def test_forecast_config_defaults():
    """Verify default target settings load correctly."""
    config = ForecastConfig()
    assert config.nfis_target_2027 == 60.0
    assert config.confidence_interval == 0.95

def test_missing_years_interpolation():
    """Test interpolation on sparse survey years."""
    data = pd.DataFrame({
        "year": [2011, 2014, 2017, 2021, 2024],
        "indicator_value": [22.0, 28.0, np.nan, 46.0, 52.0]
    })
    interpolated = data["indicator_value"].interpolate(method="linear")
    assert not interpolated.isna().any()
    assert interpolated.iloc[2] == pytest.approx(37.0)

def test_unmatched_event_impact_links():
    """Test safety filter for unlinked policy events."""
    events_df = pd.DataFrame([
        {"event_id": "EVT_01", "event_name": "Telebirr Launch", "impact_link": "ACC_MOB_MONEY"},
        {"event_id": "EVT_02", "event_name": "Unlinked Policy Shift", "impact_link": None}
    ])
    valid_events = events_df[events_df["impact_link"].notna()]
    assert len(valid_events) == 1
    assert "EVT_02" not in valid_events["event_id"].values

def test_scenario_multipliers():
    """Verify scenario multiplier logic."""
    scenario = ScenarioConfig()
    multipliers = scenario.multipliers
    assert multipliers["pessimistic"] < multipliers["base"] < multipliers["optimistic"]