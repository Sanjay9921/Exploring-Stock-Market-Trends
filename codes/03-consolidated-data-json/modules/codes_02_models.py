# codes/03-consolidated-data-json/modules/codes_02_models.py

from pathlib import Path
import sys

# Ensure Module 2 package is on sys.path
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parents[2]
MODULE2_DIR = ROOT_DIR / "codes" / "02-unified-wealth-migration"

if str(MODULE2_DIR) not in sys.path:
    sys.path.append(str(MODULE2_DIR))

from modules.models import Account, Asset, Holding  # type: ignore

__all__ = ["Account", "Asset", "Holding"]
