from datetime import datetime, timezone

import pandas as pd

from .config import BRONZE_DIR, RAW_DIR, ensure_dirs

DTYPES = {
    "order_id": "string",
    "customer_id": "string",
    "product": "string",
    "category": "string",
    "quantity": "int64",
    "unit_price": "float64",
    "country": "string",
    "created_at": "string",
}


def ingest_to_bronze() -> pd.DataFrame:
    """Reads every raw CSV partition and writes a typed, deduplicated-by-ingestion Parquet file to bronze."""
    ensure_dirs()

    csv_files = sorted(RAW_DIR.glob("dt=*/sales.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No raw data found under {RAW_DIR}. Run the 'generate' step first.")

    frames = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(frames, ignore_index=True).astype(DTYPES)
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()

    out_path = BRONZE_DIR / "sales.parquet"
    df.to_parquet(out_path, index=False)
    return df
