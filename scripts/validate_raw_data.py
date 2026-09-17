from pathlib import Path

import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def validate_raw_data() -> None:
    parquet_files = sorted(RAW_DIR.glob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(f"No Parquet files found in {RAW_DIR}")

    for path in parquet_files:
        table = pq.read_table(path)

        print(f"{path.name}: {table.num_rows:,} rows, {table.num_columns} columns")


if __name__ == "__main__":
    validate_raw_data()
