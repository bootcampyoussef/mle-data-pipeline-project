from pathlib import Path

import polars as pl

from prefect import flow, task, get_run_logger

from data_pipeline.extract import extract_parquet
from data_pipeline.transform import transform_rides
from data_pipeline.load import load_parquet


@task
def extract_task(file_path: Path) -> pl.DataFrame:
    logger = get_run_logger()
    logger.info("Extracting data from %s", file_path)

    rides = extract_parquet(file_path)

    logger.info("Extracted rows %s ", f"{rides.height:,}")

    return rides


@task
def load_task(df: pl.DataFrame, output_path: Path) -> None:
    logger = get_run_logger()
    logger.info("Loading data into %s", output_path)

    load_parquet(df, output_path)


@task
def transform_task(df: pl.DataFrame) -> pl.DataFrame:

    logger = get_run_logger()
    logger.info("Transforming row %s ", f"{df.height:,}")
    transformed_rides = transform_rides(df)

    logger.info(
        "Rows nach Transformation : %s",
        f"{transformed_rides.height:,}",
    )

    return transformed_rides


@flow(name="green-taxi-etl")
def run_prefect_pipeline(
    raw_dir: Path,
    processed_dir: Path,
) -> None:
    logger = get_run_logger()

    input_files = sorted(raw_dir.glob("green_tripdata_*.parquet"))

    if not input_files:
        raise FileNotFoundError(f"No green taxi parquet file gefunden in {raw_dir}")
    logger.info("found %s input files ", len(input_files))

    for input_path in input_files:
        rides = extract_task(input_path)

        transformed_rides = transform_task(rides)

        output_path = processed_dir / input_path.name

        load_task(transformed_rides, output_path)

    logger.info("Pipeline completed successfuly")


@task(retries=2, retry_delay_seconds=3)
def extract_task(file_path: Path) -> pl.DataFrame:

    logger = get_run_logger()
    logger.info("Extracting data from %s ", file_path)

    rides = extract_parquet(file_path)

    logger.info("Extracted rows %s", f"{rides.height:,}")

    return rides
