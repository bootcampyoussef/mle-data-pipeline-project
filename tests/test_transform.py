from datetime import datetime

import polars as pl
import pytest

from data_pipeline.transform import transform_rides


def test_transform_rides() -> None:

    rides = pl.DataFrame(
        {
            "lpep_pickup_datetime": [
                datetime(2025, 1, 1, 10, 0),
                datetime(2025, 1, 1, 11, 0),
                datetime(2025, 1, 1, 12, 0),
            ],
            "lpep_dropoff_datetime": [
                datetime(2025, 1, 1, 10, 30),
                datetime(2025, 1, 1, 11, 20),
                datetime(2025, 1, 1, 11, 50),
            ],
            "trip_distance": [
                5.0,
                0.0,
                3.0,
            ],
            "total_amount": [
                25.0,
                15.0,
                20.0,
            ],
        }
    )
    result = transform_rides(rides)

    assert result.height == 1
    assert "pickup_date" in result.columns
    assert "trip_duration_minutes" in result.columns
    assert result["trip_distance"][0] == 5.0
    assert result["trip_duration_minutes"][0] == 30


def test_transform_rides_missing_column() -> None:

    rides = pl.DataFrame(
        {
            "trip_distance": [5.0],
            "total_amount": [20.0],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_rides(rides)
