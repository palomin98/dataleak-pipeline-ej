import pandas as pd

from .config import BRONZE_DIR, SILVER_DIR, ensure_dirs


def transform_to_silver() -> pd.DataFrame:
    """Cleans bronze data: drops duplicate orders and invalid rows, adds derived fields."""
    ensure_dirs()

    bronze_path = BRONZE_DIR / "sales.parquet"
    if not bronze_path.exists():
        raise FileNotFoundError(f"No bronze data found at {bronze_path}. Run the 'bronze' step first.")

    df = pd.read_parquet(bronze_path)

    df = df.drop_duplicates(subset="order_id")
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)

    out_path = SILVER_DIR / "sales.parquet"
    df.to_parquet(out_path, index=False)
    return df
