import pytest
import pandas as pd
from src.data_loader import DataLoader

def test_data_loader_structure():
    loader = DataLoader(data_dir="data/raw")
    try:
        obs, events, impacts, targets = loader.get_parsed_records()
        assert isinstance(obs, pd.DataFrame)
        assert isinstance(events, pd.DataFrame)
        assert isinstance(impacts, pd.DataFrame)
        assert isinstance(targets, pd.DataFrame)
    except FileNotFoundError:
        pytest.skip("Raw data files not present in local path; skipping dataset test.")