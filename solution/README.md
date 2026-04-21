# Reference Solution

This folder contains a complete local-first reference implementation for this project.

### What the solution does

1. Downloads `green_tripdata_2025-01.parquet`, `green_tripdata_2025-02.parquet` and `green_tripdata_2025-03.parquet` into `solution/data/raw/`.
2. Reads those parquet files locally.
3. Aggregates `total_amount` by pickup date to produce daily revenue.
4. Writes outputs to `solution/data/processed/` as CSV, parquet and JSON metadata.
5. Includes an optional Prefect flow for the bonus orchestration task.

### Project structure

- [solution/src/data_pipeline/cli.py](solution/src/data_pipeline/cli.py) exposes `download`, `run` and `all` commands.
- [solution/src/data_pipeline/download.py](solution/src/data_pipeline/download.py) handles dataset downloads.
- [solution/src/data_pipeline/prefect_flow.py](solution/src/data_pipeline/prefect_flow.py) contains the optional Prefect flow.
- [solution/src/data_pipeline/transform.py](solution/src/data_pipeline/transform.py) calculates daily revenue and writes outputs.
- [solution/tests/test_transform.py](solution/tests/test_transform.py) covers the revenue aggregation logic.

### Run the reference solution

### **`macOS`**

```bash
cd solution
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
pytest
```

### **`Windows`**

For `PowerShell` CLI:

```PowerShell
cd solution
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
pytest
```

For `Git-Bash` CLI:

```bash
cd solution
py -3 -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
pytest
```

[requirements.txt](./requirements.txt) pins the exact dependency versions that were used for this solution.

### Optional bonus flow

```bash
python scripts/run_prefect_flow.py
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
