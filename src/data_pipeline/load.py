from pathlib import Path

import polars as pl


def load_parquet(df: pl.DataFrame, output_path: Path) -> None:
    """Write parquet to file"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)
