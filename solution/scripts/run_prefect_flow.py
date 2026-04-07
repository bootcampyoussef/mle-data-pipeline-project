import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_pipeline.prefect_flow import green_taxi_local_pipeline


if __name__ == "__main__":
    green_taxi_local_pipeline()
