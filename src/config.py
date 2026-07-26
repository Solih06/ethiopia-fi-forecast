import os
from dataclasses import dataclass, field
from typing import Dict, Set

# Base Directories
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR: str = os.path.join(BASE_DIR, "data", "raw")

# File Paths
UNIFIED_DATA_PATH: str = os.path.join(DATA_DIR, "ethiopia_fi_unified_data.csv")
REF_CODES_PATH: str = os.path.join(DATA_DIR, "reference_codes.csv")

# Core Schema Required Columns Across All Record Types
REQUIRED_COLUMNS: list[str] = [
    'record_type', 'indicator_code', 'value_numeric'
]

# Record Types
VALID_RECORD_TYPES: Set[str] = {'observation', 'event', 'impact_link', 'target'}

# Primary Policy Targets (NFIS-II Policy Targets)
NFIS_TARGET_2027: float = 60.0
NFIS_TARGET_2030: float = 70.0


# --- Centralized Indicator Codes & Scenario Configurations ---

@dataclass(frozen=True)
class IndicatorCodes:
    """Core indicator mapping for Findex and administrative data sources."""
    ACCOUNT_OWNERSHIP: str = "ACC_OWN_ADULT"
    MOBILE_MONEY_ACCOUNT: str = "ACC_MOB_MONEY"
    DIGITAL_PAYMENTS: str = "PAY_DIGITAL_12M"
    USAGE_FREQUENCY: str = "USE_FREQ_MONTHLY"


@dataclass
class ScenarioConfig:
    """Configuration for scenario multipliers and forecasting parameters."""
    start_year: int = 2025
    end_year: int = 2027
    default_lag_months: int = 6
    
    # Scenario multipliers for event impact adjustments
    multipliers: Dict[str, float] = field(
        default_factory=lambda: {
            "pessimistic": 0.75,
            "base": 1.0,
            "optimistic": 1.25,
        }
    )
@dataclass
class ForecastConfig:
    """Wrapper configuration for forecasting parameters and NFIS targets."""
    start_year: int = 2025
    end_year: int = 2027
    nfis_target_2027: float = NFIS_TARGET_2027
    nfis_target_2030: float = NFIS_TARGET_2030
    confidence_interval: float = 0.95
    indicator_codes: IndicatorCodes = field(default_factory=IndicatorCodes)
    scenario: ScenarioConfig = field(default_factory=ScenarioConfig)