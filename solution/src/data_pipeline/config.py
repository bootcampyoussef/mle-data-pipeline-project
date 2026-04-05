from __future__ import annotations

from pathlib import Path

DEFAULT_MONTHS = ("2025-01", "2025-02", "2025-03")
DEFAULT_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DEFAULT_FILENAME_TEMPLATE = "green_tripdata_{month}.parquet"
DEFAULT_DOWNLOAD_TIMEOUT_SECONDS = 60

SOLUTION_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = SOLUTION_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def build_dataset_filename(month: str) -> str:
    return DEFAULT_FILENAME_TEMPLATE.format(month=month)


def build_dataset_url(month: str, base_url: str = DEFAULT_BASE_URL) -> str:
    return f"{base_url.rstrip('/')}/{build_dataset_filename(month)}"
