import polars as pl

REQUIRED_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_distance",
    "total_amount",
]


def transform_rides(df: pl.DataFrame) -> pl.DataFrame:
    """clean and enrich taxi ride data"""

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return (
        df.drop_nulls(REQUIRED_COLUMNS)
        .filter(
            (pl.col("trip_distance") > 0)
            & (pl.col("total_amount") >= 0)
            & (pl.col("tpep_dropoff_datetime") >= pl.col("tpep_pickup_datetime"))
        )
        .with_columns(
            [
                pl.col("tpep_pickup_datetime").dt.date().alias("pickup_date"),
                (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime"))
                .dt.total_minutes()
                .alias("trip_duration_minutes"),
            ]
        )
    )
