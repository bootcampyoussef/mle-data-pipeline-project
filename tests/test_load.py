from pathlib import Path

import polars as pl

from data_pipeline.load import load_parquet


def test_load_parquet(tmp_path: Path) -> None:
    output_file = tmp_path / "processed" / "rides_parquet"

    expected = pl.DataFrame(
        {
            "trip_distance": [2.5, 5.0],
            "total_amount": [15.0, 30.0],
        }
    )

    load_parquet(expected, output_file)

    assert output_file.exists()

    result = pl.read_parquet(output_file)

    assert result.equals(expected)
