import pandas as pd

from .config import GOLD_DIR, SILVER_DIR, ensure_dirs


def build_gold() -> dict[str, pd.DataFrame]:
    """Aggregates silver data into business-ready summary tables."""
    ensure_dirs()

    silver_path = SILVER_DIR / "sales.parquet"
    if not silver_path.exists():
        raise FileNotFoundError(f"No silver data found at {silver_path}. Run the 'silver' step first.")

    df = pd.read_parquet(silver_path)

    by_category = (
        df.groupby("category")
        .agg(orders=("order_id", "count"), total_revenue=("total_amount", "sum"))
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    daily_revenue = (
        df.assign(dt=df["created_at"].dt.date)
        .groupby("dt")
        .agg(orders=("order_id", "count"), total_revenue=("total_amount", "sum"))
        .reset_index()
        .sort_values("dt")
    )

    by_category.to_parquet(GOLD_DIR / "revenue_by_category.parquet", index=False)
    daily_revenue.to_parquet(GOLD_DIR / "daily_revenue.parquet", index=False)

    return {"revenue_by_category": by_category, "daily_revenue": daily_revenue}
