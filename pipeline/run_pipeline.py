from .bronze import ingest_to_bronze
from .gold import build_gold
from .silver import transform_to_silver


def run_pipeline() -> None:
    bronze_df = ingest_to_bronze()
    print(f"[bronze] {len(bronze_df)} rows ingested")

    silver_df = transform_to_silver()
    print(f"[silver] {len(silver_df)} rows after cleaning ({len(bronze_df) - len(silver_df)} dropped)")

    gold_tables = build_gold()
    for name, table in gold_tables.items():
        print(f"[gold] {name}: {len(table)} rows")
