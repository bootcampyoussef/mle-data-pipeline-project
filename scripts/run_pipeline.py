from pathlib import Path

from data_pipeline.extract import extract_parquet
from data_pipeline.load import load_parquet
from data_pipeline.transform import transform_rides

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def run_pipeline() -> None:
    """run complete pipeline"""

    input_files = sorted(RAW_DIR.glob("green_tripdata_*.parquet"))

    if not input_files:
        raise FileNotFoundError(f"No Green Taxi parquet files found")

    for input_path in input_files:
        print(f"\nExtracting data from: {input_path}")
        rides = extract_parquet(input_path)
        print(f"Extracted {rides.height:,} rows")

        print(f"Transforming data ....")
        transformed_rides = transform_rides(rides)

        print(f"Rows afer transformation : {transformed_rides.height:,}")

        output_path = PROCESSED_DIR / input_path.name

        print(f"loading data to : {output_path}")
        load_parquet(transformed_rides, output_path)

    print(f"Pipeline completed successfuly w")


if __name__ == "__main__":
    run_pipeline()
