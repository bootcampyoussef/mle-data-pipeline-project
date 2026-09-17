from pathlib import Path

import polars as pl
import pytest

from data_pipeline.extract import extract_parquet


def test_extract_parquet(tmp_path: Path) -> None:
    input_file = tmp_path / "test_data.parquet"

    expected = pl.DataFrame(
        {
            "trip_id": [1, 2, 3],
            "distance": [2.5, 4.0, 8.3],
        }
    )

    expected.write_parquet(input_file)

    result = extract_parquet(input_file)

    assert isinstance(result, pl.DataFrame)
    assert result.equals(expected)


def test_extract_parquet_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.parquet"

    with pytest.raises(FileNotFoundError):
        extract_parquet(missing_file)
