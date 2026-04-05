from __future__ import annotations

import argparse
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


def parse_months(raw_months: str | None) -> list[str]:
    if not raw_months:
        return list(DEFAULT_MONTHS)
    return [month.strip() for month in raw_months.split(",") if month.strip()]


def collect_input_paths(raw_dir: Path, months: list[str]) -> list[Path]:
    paths = [raw_dir / build_dataset_filename(month) for month in months]
    missing_paths = [path for path in paths if not path.exists()]
    if missing_paths:
        missing_text = ", ".join(path.name for path in missing_paths)
        raise FileNotFoundError(
            f"Missing expected input files in {raw_dir}: {missing_text}. Run the download step first."
        )
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local-first reference solution for the NYC Green Taxi pipeline project."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser(
        "download", help="Download the source parquet files."
    )
    download_parser.add_argument(
        "--months", help="Comma-separated list like 2025-01,2025-02,2025-03."
    )
    download_parser.add_argument("--raw-dir", default=str(RAW_DIR))
    download_parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    download_parser.add_argument("--force", action="store_true")

    run_parser = subparsers.add_parser(
        "run", help="Transform raw parquet files into daily revenue outputs."
    )
    run_parser.add_argument(
        "--months", help="Comma-separated list like 2025-01,2025-02,2025-03."
    )
    run_parser.add_argument("--raw-dir", default=str(RAW_DIR))
    run_parser.add_argument("--output-dir", default=str(PROCESSED_DIR))

    all_parser = subparsers.add_parser(
        "all", help="Run download and transformation in sequence."
    )
    all_parser.add_argument(
        "--months", help="Comma-separated list like 2025-01,2025-02,2025-03."
    )
    all_parser.add_argument("--raw-dir", default=str(RAW_DIR))
    all_parser.add_argument("--output-dir", default=str(PROCESSED_DIR))
    all_parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    all_parser.add_argument("--force", action="store_true")

    return parser


def handle_download(
    raw_dir: Path, months: list[str], base_url: str, force: bool
) -> int:
    results = download_months(months, raw_dir, base_url=base_url, force=force)
    for result in results:
        action = "downloaded" if result.downloaded else "reused"
        print(f"{action}: {result.destination}")
    return 0


def handle_run(raw_dir: Path, output_dir: Path, months: list[str]) -> int:
    input_paths = collect_input_paths(raw_dir, months)
    outputs, metadata = run_pipeline(input_paths, output_dir)
    print(f"wrote: {outputs.daily_revenue_csv}")
    print(f"wrote: {outputs.daily_revenue_parquet}")
    print(f"wrote: {outputs.metadata_json}")
    print(
        "summary:"
        f" days={metadata['days_in_output']}"
        f", trips={metadata['trips_in_output']}"
        f", revenue_total={metadata['revenue_total']}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    months = parse_months(args.months)
    raw_dir = Path(args.raw_dir)

    if args.command == "download":
        return handle_download(raw_dir, months, args.base_url, args.force)

    if args.command == "run":
        return handle_run(raw_dir, Path(args.output_dir), months)

    if args.command == "all":
        handle_download(raw_dir, months, args.base_url, args.force)
        return handle_run(raw_dir, Path(args.output_dir), months)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
