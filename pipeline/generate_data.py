import random
from datetime import date, timedelta

import pandas as pd

from .config import RAW_DIR, ensure_dirs

PRODUCTS = {
    "Laptop": "Electronics",
    "Phone": "Electronics",
    "Headphones": "Electronics",
    "Desk Chair": "Furniture",
    "Bookshelf": "Furniture",
    "Coffee Maker": "Appliances",
    "Blender": "Appliances",
    "Novel": "Books",
    "Cookbook": "Books",
}

COUNTRIES = ["ES", "FR", "DE", "IT", "PT"]


def generate_sales_events(day: date, n_rows: int, seed: int | None = None) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for i in range(n_rows):
        product = rng.choice(list(PRODUCTS.keys()))
        rows.append(
            {
                "order_id": f"{day.isoformat()}-{i:05d}",
                "customer_id": f"cust-{rng.randint(1, 500):04d}",
                "product": product,
                "category": PRODUCTS[product],
                "quantity": rng.randint(1, 5),
                "unit_price": round(rng.uniform(5, 500), 2),
                "country": rng.choice(COUNTRIES),
                "created_at": day.isoformat(),
            }
        )

    # introduce a bit of messy data on purpose, to give the silver layer something to clean
    if rows:
        dirty_idx = rng.randint(0, len(rows) - 1)
        rows[dirty_idx]["quantity"] = -1
        rows.append(dict(rows[0]))  # duplicate order

    return pd.DataFrame(rows)


def write_raw_day(day: date, n_rows: int, seed: int | None = None) -> None:
    ensure_dirs()
    df = generate_sales_events(day, n_rows, seed=seed)
    day_dir = RAW_DIR / f"dt={day.isoformat()}"
    day_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(day_dir / "sales.csv", index=False)


def generate_raw_history(days: int, rows_per_day: int, seed: int | None = None) -> list[date]:
    today = date.today()
    generated = []
    for offset in range(days):
        day = today - timedelta(days=offset)
        write_raw_day(day, rows_per_day, seed=seed)
        generated.append(day)
    return generated
