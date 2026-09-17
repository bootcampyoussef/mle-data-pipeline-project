from pathlib import Path

import polars as pl


def extract_parquet(file_path: Path) -> pl.DataFrame:
    """Load a Parquet file into a Polar DataFrame"""

    if not file_path.exists():
        raise FileNotFoundError(f"input file not found : {file_path}")

    return pl.read_parquet(file_path)
