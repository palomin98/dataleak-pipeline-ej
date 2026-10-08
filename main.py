import argparse

import pandas as pd

from pipeline.config import BRONZE_DIR, GOLD_DIR, RAW_DIR, SILVER_DIR
from pipeline.generate_data import generate_raw_history
from pipeline.run_pipeline import run_pipeline

LAYER_DIRS = {
    "raw": RAW_DIR,
    "bronze": BRONZE_DIR,
    "silver": SILVER_DIR,
    "gold": GOLD_DIR,
}


def cmd_generate(args: argparse.Namespace) -> None:
    days = generate_raw_history(args.days, args.rows_per_day, seed=args.seed)
    print(f"Generated {args.days} day(s) of raw data ({args.rows_per_day} rows/day) under {RAW_DIR}")
    print(f"Dates: {', '.join(d.isoformat() for d in days)}")


def cmd_run(args: argparse.Namespace) -> None:
    run_pipeline()


def cmd_all(args: argparse.Namespace) -> None:
    cmd_generate(args)
    run_pipeline()


def cmd_show(args: argparse.Namespace) -> None:
    layer_dir = LAYER_DIRS[args.layer]
    parquet_files = sorted(layer_dir.glob("*.parquet")) if args.layer != "raw" else []

    if args.layer == "raw":
        csv_files = sorted(RAW_DIR.glob("dt=*/sales.csv"))
        if not csv_files:
            print(f"No data found in raw layer ({RAW_DIR}). Run 'generate' first.")
            return
        df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        print(df.head(args.rows))
        return

    if not parquet_files:
        print(f"No data found in {args.layer} layer ({layer_dir}). Run 'run' first.")
        return

    for f in parquet_files:
        print(f"\n--- {f.name} ---")
        print(pd.read_parquet(f).head(args.rows))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small local data lake pipeline (raw -> bronze -> silver -> gold).")
    sub = parser.add_subparsers(dest="command", required=True)

    p_generate = sub.add_parser("generate", help="Generate synthetic raw sales data")
    p_generate.add_argument("--days", type=int, default=3, help="Number of days of history to generate")
    p_generate.add_argument("--rows-per-day", type=int, default=200, help="Rows generated per day")
    p_generate.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p_generate.set_defaults(func=cmd_generate)

    p_run = sub.add_parser("run", help="Run bronze -> silver -> gold on existing raw data")
    p_run.set_defaults(func=cmd_run)

    p_all = sub.add_parser("all", help="Generate data and run the full pipeline")
    p_all.add_argument("--days", type=int, default=3)
    p_all.add_argument("--rows-per-day", type=int, default=200)
    p_all.add_argument("--seed", type=int, default=None)
    p_all.set_defaults(func=cmd_all)

    p_show = sub.add_parser("show", help="Preview a layer of the data lake")
    p_show.add_argument("layer", choices=["raw", "bronze", "silver", "gold"])
    p_show.add_argument("--rows", type=int, default=10)
    p_show.set_defaults(func=cmd_show)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
