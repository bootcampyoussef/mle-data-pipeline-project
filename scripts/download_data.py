from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


MONTHS = [
    "2025-01",
    "2025-02",
    "2025-03",
]


def download_data() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for month in MONTHS:
        filename = f"green_tripdata_{month}.parquet"
        url = f"{BASE_URL}/{filename}"
        destination = RAW_DIR / filename

        print(f"Downloading {url}")

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        destination.write_bytes(response.content)

        print(f"Saved to {destination}")


if __name__ == "__main__":
    download_data()
