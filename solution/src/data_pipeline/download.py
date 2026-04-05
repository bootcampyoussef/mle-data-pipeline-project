from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests

from .config import (
    DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
    RAW_DIR,
    build_dataset_filename,
    build_dataset_url,
)


@dataclass(frozen=True)
class DownloadResult:
    month: str
    destination: Path
    downloaded: bool


def download_month(
    month: str,
    raw_dir: Path = RAW_DIR,
    *,
    base_url: str,
    force: bool = False,
    timeout_seconds: int = DEFAULT_DOWNLOAD_TIMEOUT_SECONDS,
) -> DownloadResult:
    raw_dir.mkdir(parents=True, exist_ok=True)
    destination = raw_dir / build_dataset_filename(month)

    if destination.exists() and not force:
        return DownloadResult(month=month, destination=destination, downloaded=False)

    url = build_dataset_url(month, base_url)
    with requests.get(url, stream=True, timeout=timeout_seconds) as response:
        response.raise_for_status()
        with destination.open("wb") as output_file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output_file.write(chunk)

    return DownloadResult(month=month, destination=destination, downloaded=True)


def download_months(
    months: Iterable[str],
    raw_dir: Path = RAW_DIR,
    *,
    base_url: str,
    force: bool = False,
) -> list[DownloadResult]:
    return [
        download_month(month, raw_dir, base_url=base_url, force=force)
        for month in months
    ]
