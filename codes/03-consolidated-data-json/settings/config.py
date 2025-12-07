# codes/03-consolidated-data-json/settings/config.py

from pathlib import Path

# This file: .../Exploring-Stock-Market-Trends/codes/03-consolidated-data-json/settings/config.py
# parents[0] = settings
# parents[1] = 03-consolidated-data-json
# parents[2] = codes
# parents[3] = Exploring-Stock-Market-Trends  ← repo root

ROOT_DIR = Path(__file__).resolve().parents[3]

# Path to Module 2 (unified-wealth-migration)
UNIFIED_MODULE_DIR = ROOT_DIR / "codes" / "02-unified-wealth-migration"
UNIFIED_DATA_DIR = UNIFIED_MODULE_DIR / "data"
UNIFIED_MIGRATED_DIR = UNIFIED_DATA_DIR / "migrated_data"

DB_PATH = UNIFIED_MIGRATED_DIR / "portfolio.db"
DB_URI = f"sqlite:///{DB_PATH}"

# Path to ticker data from Module 1
BROKER_MODULE_DIR = ROOT_DIR / "codes" / "01-broker-simulator"
TICKER_DATA_DIR = BROKER_MODULE_DIR / "data" / "ticker_data"
COMPANIES_CSV = TICKER_DATA_DIR / "companies.csv"

EXPORT_DIR = Path(__file__).resolve().parents[1] / "data" / "json_exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
