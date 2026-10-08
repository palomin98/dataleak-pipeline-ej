from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_LAKE_DIR = BASE_DIR / "data_lake"

RAW_DIR = DATA_LAKE_DIR / "raw" / "sales"
BRONZE_DIR = DATA_LAKE_DIR / "bronze" / "sales"
SILVER_DIR = DATA_LAKE_DIR / "silver" / "sales"
GOLD_DIR = DATA_LAKE_DIR / "gold" / "sales"


def ensure_dirs() -> None:
    for d in (RAW_DIR, BRONZE_DIR, SILVER_DIR, GOLD_DIR):
        d.mkdir(parents=True, exist_ok=True)
