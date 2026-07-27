from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass(frozen=True)
class MatrixConfig:
    FILE_PATH: str = "data/processed/event_association_matrix.csv"
    REQUIRED_COLUMNS: tuple = (
        "event_id",
        "event_name",
        "year",
        "policy_type",
        "target_indicator",
        "impact_shift_pp",
    )


def load_event_association_matrix(filepath: Optional[str] = None) -> pd.DataFrame:
    """Loads, validates, and processes the quantitative Policy Event Association Matrix."""
    path = filepath or MatrixConfig.FILE_PATH
    df = pd.read_csv(path)

    missing_cols = set(MatrixConfig.REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Matrix dataset missing required columns: {missing_cols}")

    return df


def calculate_total_impact_shift(df: pd.DataFrame, target_indicator: str) -> float:
    """Calculates cumulative percentage-point (+pp) impact shift for a specific indicator."""
    filtered = df[df["target_indicator"] == target_indicator]
    return float(filtered["impact_shift_pp"].sum())


if __name__ == "__main__":
    matrix = load_event_association_matrix()
    print("Successfully loaded Event Association Matrix:\n")
    print(matrix.to_string(index=False))
