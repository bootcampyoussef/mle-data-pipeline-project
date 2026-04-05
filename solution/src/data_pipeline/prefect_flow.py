from __future__ import annotations

import importlib
from pathlib import Path

from .config import (
    DEFAULT_BASE_URL,
    DEFAULT_MONTHS,
    PROCESSED_DIR,
    RAW_DIR,
    build_dataset_filename,
)
from .download import download_months
from .transform import run_pipeline


def download_step(months: list[str], raw_dir: Path, base_url: str, force: bool) -> None:
    download_months(months, raw_dir, base_url=base_url, force=force)


def transform_step(
    months: list[str], raw_dir: Path, output_dir: Path
) -> dict[str, object]:
    input_paths = [raw_dir / build_dataset_filename(month) for month in months]
    _, metadata = run_pipeline(input_paths, output_dir)
    return metadata


def green_taxi_local_pipeline(
    months: list[str] | None = None,
    raw_dir: Path = RAW_DIR,
    output_dir: Path = PROCESSED_DIR,
    base_url: str = DEFAULT_BASE_URL,
    force: bool = False,
) -> dict[str, object]:
    try:
        prefect = importlib.import_module("prefect")
    except (
        ImportError
    ) as error:  # pragma: no cover - exercised only when Prefect is missing
        raise ImportError(
            "Prefect is not installed. Install the optional orchestration dependencies with "
            "'pip install -e .[orchestration]'."
        ) from error

    flow = prefect.flow
    task = prefect.task

    selected_months = months or list(DEFAULT_MONTHS)

    @task
    def download_task(
        task_months: list[str],
        task_raw_dir: Path,
        task_base_url: str,
        task_force: bool,
    ) -> None:
        download_step(task_months, task_raw_dir, task_base_url, task_force)

    @task
    def transform_task(
        task_months: list[str],
        task_raw_dir: Path,
        task_output_dir: Path,
    ) -> dict[str, object]:
        return transform_step(task_months, task_raw_dir, task_output_dir)

    @flow(name="green-taxi-local-pipeline")
    def pipeline_flow() -> dict[str, object]:
        download_task(selected_months, raw_dir, base_url, force)
        return transform_task(selected_months, raw_dir, output_dir)

    return pipeline_flow()
