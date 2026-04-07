# Data Pipeline Project

Please do not fork this repository. Use it as a template for your own project repository, create Pull Requests even if you work alone, and mark the checkboxes in your PR description once you finish each topic.

## Project Brief

In this project you are going to build a data pipeline that processes the `Green Taxi Trips` portion of the NYC Taxi Trip Dataset.

1. Write a script that downloads the data for the first three months of 2025 and stores it in a local staging directory.
2. Write an ETL or ELT pipeline that reads those locally staged files, processes the data, and calculates the revenue per day.

Bonus task if you have time:

1. Use Prefect for workflow orchestration.

This version of the project is intentionally local-first. You do not need GCP, GCS, or any other cloud platform to complete it.

## Questions

Your submission README should answer these questions:

1. What are the steps you took to complete the project?
2. What challenges did you face?
3. What would you do differently if you had more time?

## Submission

Submit your solution as a link to a GitHub repository. The repository should contain your scripts and a README that answers the questions above.

## Reference Solution

This repository now includes a complete local reference implementation in [solution](solution).

### What the solution does

1. Downloads `green_tripdata_2025-01.parquet`, `green_tripdata_2025-02.parquet`, and `green_tripdata_2025-03.parquet` into `solution/data/raw/`.
2. Reads those parquet files locally.
3. Aggregates `total_amount` by pickup date to produce daily revenue.
4. Writes outputs to `solution/data/processed/` as CSV, parquet, and JSON metadata.
5. Includes an optional Prefect flow for the bonus orchestration task.

### Project structure

- [solution/src/data_pipeline/cli.py](solution/src/data_pipeline/cli.py) exposes `download`, `run`, and `all` commands.
- [solution/src/data_pipeline/download.py](solution/src/data_pipeline/download.py) handles dataset downloads.
- [solution/src/data_pipeline/transform.py](solution/src/data_pipeline/transform.py) calculates daily revenue and writes outputs.
- [solution/src/data_pipeline/prefect_flow.py](solution/src/data_pipeline/prefect_flow.py) contains the optional Prefect flow.
- [solution/tests/test_transform.py](solution/tests/test_transform.py) covers the revenue aggregation logic.

### Run the reference solution

`macOS` / Linux:

```bash
cd solution
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest
```

`requirements.txt` pins the exact dependency versions that were tested with this solution.

`Windows`:

```bash
cd solution
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\run_pipeline.py
pytest
```

Optional bonus flow:

`macOS` / Linux:

```bash
cd solution
source .venv/bin/activate
pip install prefect==3.6.25
python scripts/run_prefect_flow.py
```

`Windows`:

```bash
cd solution
.venv\Scripts\activate
pip install prefect==3.6.25
python scripts\run_prefect_flow.py
```

The helper scripts add `solution/src/` to `PYTHONPATH` automatically, so you do not need an editable package install.

### Expected outputs

After a successful run, you should see:

- `solution/data/raw/green_tripdata_2025-01.parquet`
- `solution/data/raw/green_tripdata_2025-02.parquet`
- `solution/data/raw/green_tripdata_2025-03.parquet`
- `solution/data/processed/daily_revenue.csv`
- `solution/data/processed/daily_revenue.parquet`
- `solution/data/processed/pipeline_metadata.json`
