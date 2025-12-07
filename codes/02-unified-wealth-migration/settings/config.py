# codes/02-unified-wealth-migration/settings/config.py

from pathlib import Path

# Root of the repo: one level up from /codes
ROOT_DIR = Path(__file__).resolve().parents[2]  # OLD (gives ...\Projects\Exploring-Stock-Market-Trends)
# In your actual layout it's:
# Exploring-Stock-Market-Trends/
#   codes/
#     01-broker-simulator/
#     02-unified-wealth-migration/

# Since config.py is in: .../codes/02-unified-wealth-migration/settings/config.py
# parents[0] = settings
# parents[1] = 02-unified-wealth-migration
# parents[2] = codes
# parents[3] = Exploring-Stock-Market-Trends  ← correct root

ROOT_DIR = Path(__file__).resolve().parents[3]  # ✅ use parents[3]

# Location of broker-simulator outputs
BROKER_MODULE_DIR = ROOT_DIR / "codes" / "01-broker-simulator"
BROKER_RAW_DATA_DIR = BROKER_MODULE_DIR / "data" / "raw_data"

RAW_POSITIONS_PATH = BROKER_RAW_DATA_DIR / "raw_positions.csv"
RAW_PRICES_PATH = BROKER_RAW_DATA_DIR / "raw_prices.csv"

# SQLite DB location for unified wealth data
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "migrated_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "portfolio.db"
DB_URI = f"sqlite:///{DB_PATH}"

TEST_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "test_data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)