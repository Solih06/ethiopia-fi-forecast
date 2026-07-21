import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# File Paths
UNIFIED_DATA_PATH = os.path.join(DATA_DIR, "ethiopia_fi_unified_data.csv")
REF_CODES_PATH = os.path.join(DATA_DIR, "reference_codes.csv")

# Expected Unified Schema Columns
REQUIRED_COLUMNS = [
    'record_type', 'indicator_code', 'value_numeric', 'year', 'observation_date'
]

# Record Types
VALID_RECORD_TYPES = {'observation', 'event', 'impact_link', 'target'}

# Primary Policy Targets (NFIS-II Policy Targets)
NFIS_TARGET_2027 = 60.0
NFIS_TARGET_2030 = 70.0