# Solution

This folder contains a complete local-first reference implementation for the project prompt in the repository root README.

Use the commands from the root README to install dependencies, download the 2025 Green Taxi parquet files, and build the daily revenue outputs.

## Answers To The Project Questions

### 1. What are the steps you took to complete the project?

<details>
<summary>Show answer</summary>

1. Defined a local-first version of the assignment so the workflow no longer depends on GCP.
2. Added a download step that stages the NYC TLC parquet files in a raw data folder.
3. Built a transformation step that reads the raw files and aggregates `total_amount` by pickup date.
4. Wrote the results to CSV, parquet, and JSON metadata files.
5. Added tests for the revenue calculation logic and an optional Prefect flow for orchestration.

</details>

### 2. What challenges did you face?

<details>
<summary>Show answer</summary>

1. The original prompt assumed a cloud bucket, so the project needed a clean local equivalent that still felt realistic.
2. Taxi data schemas can vary over time, so the solution includes a fallback revenue calculation when `total_amount` is unavailable.
3. The repository originally only contained docs, so both the implementation and the final instructions had to be aligned from scratch.

</details>

### 3. What would you do differently with more time?

<details>
<summary>Show answer</summary>

1. Add data-quality checks for nulls, duplicate trips, and outlier fares.
2. Add richer logging and metrics for each pipeline stage.
3. Package the workflow with Docker and CI so it can be run the same way everywhere.
4. Expand tests to cover schema drift and larger integration scenarios.

</details>
