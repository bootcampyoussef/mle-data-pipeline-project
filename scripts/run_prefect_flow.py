from pathlib import Path
from data_pipeline.orchestration import run_prefect_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DIR = PROJECT_ROOT / "data" /"processed"


if __name__ == "__main__" :
    run_prefect_pipeline (

        raw_dir=RAW_DIR,
        processed_dir= PROCESSED_DIR,
    )



