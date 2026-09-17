from pathlib import Path

from data_pipeline.extract import extract_parquet
from data_pipeline.load import load_parquet
from data_pipeline.transform import transform_rides

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "green_tripdata_2025-01.parquet"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "green_tripdata_2025-01.parquet"


def run_pipeline() -> None:
    """run complete pipeline"""

    print(f"extrating data from : {INPUT_PATH}")
    rides = extract_parquet(INPUT_PATH)
    print(f"extrated {rides.height:,} rows")

    print(f"Transforming data ...")
    transformed_rides = transform_rides(rides)

    print(f"Loadin data to : {OUTPUT_PATH}")
    load_parquet(transformed_rides, OUTPUT_PATH)

    print(f"Pipeline completed successfuly ...")


if __name__ == "__main__":
    run_pipeline()
