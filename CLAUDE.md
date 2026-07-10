# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a LinkedIn Learning course repo demonstrating dbt Core with DuckDB. It implements the **Medallion Architecture** (bronze → silver → gold) on NYC parking violations data. The dbt project lives in `nyc_parking_violations/` and uses a local DuckDB file as the database backend.

## Setup

Install dependencies (Python 3.10 required):
```bash
pip install -r requirements.txt
```

The DuckDB database files (`data/nyc_parking_violations.db` and `data/prod_nyc_parking_violations.db`) are committed to git with the source tables (`parking_violation_codes`, `parking_violations_2023`) already loaded from the CSVs in `data/`, so `dbt run` works immediately after cloning — no seed/load step is required. `run_sql_queries_here.ipynb` is just a scratchpad for running ad hoc SQL against the dev database (e.g. `show tables`); it no longer contains the original `read_csv_auto` loading cells. To rebuild a database from the raw CSVs from scratch, see the `CREATE OR REPLACE TABLE ... FROM read_csv_auto(...)` pattern in `assets/tutorial_files/dbt_project_walkthrough.md` (Step 3).

## dbt Commands

All dbt commands must be run from the `nyc_parking_violations/` directory, where both `dbt_project.yml` and `profiles.yml` live:

```bash
cd nyc_parking_violations
dbt debug       # validate config and connection
dbt compile     # parse models and check for errors without executing SQL
dbt run         # execute all models against the dev database
dbt test        # run all data quality tests
dbt docs generate && dbt docs serve   # build and serve docs at localhost:8080
```

Run a single model:
```bash
dbt run --select bronze_parking_violations
```

Run with prod target:
```bash
dbt run --target prod
dbt test --target prod
```

## Architecture

### Data Pipeline (Medallion)

```
CSV files (data/)
    └─> DuckDB source tables (pre-loaded, committed to git)
            ├─> Bronze (views)  — raw column subset from source tables
            ├─> Silver          — cleaned + business logic applied
            │       ├─> silver_parking_violation_codes  (ephemeral)
            │       ├─> silver_parking_violations        (ephemeral)
            │       ├─> silver_violation_tickets         (view)
            │       └─> silver_violation_vehicles        (view)
            └─> Gold (tables)   — gold_ticket_metrics, gold_vehicles_metrics
```

`models/example/` (`first_model.sql`, `ref_model.sql`) is leftover scaffolding from `dbt init`, kept only to demonstrate `ref()`; it's `ephemeral` and not part of the medallion pipeline above.

### Materialization Strategy

Configured in `nyc_parking_violations/dbt_project.yml`:
- **Bronze** → `view` (infrequently queried, acceptable query wait)
- **Silver intermediaries** (`silver_parking_violation_codes`, `silver_parking_violations`) → `ephemeral` (not exposed to data consumers; inlined into downstream queries)
- **Silver final** (`silver_violation_tickets`, `silver_violation_vehicles`) → `view`
- **Gold** → `table` (pre-computed for dashboard/report consumers)

### Profiles and Environments

`profiles.yml` is in `nyc_parking_violations/` (not `~/.dbt/`). Two targets:
- `dev` — writes to `data/nyc_parking_violations.db` (relative path from the project dir)
- `prod` — writes to `data/prod_nyc_parking_violations.db` (path relative to repo root, used by GitHub Actions)

### Documentation

Documentation lives in `nyc_parking_violations/models/docs/`:
- `schema.yml` — model and column descriptions, test definitions
- `docs_blocks.md` — reusable Jinja doc blocks referenced with `'{{ doc("block_name") }}'` in `schema.yml`

### Tests

Tests are in `nyc_parking_violations/tests/`:
- **Singular tests** (e.g., `violation_codes_revenue.sql`) — SQL that returns rows on failure; configured with `{{ config(severity = 'warn') }}` to warn rather than error
- **Generic tests** (e.g., `tests/generic/generic_not_null.sql`) — Jinja-templated test functions referenced in `schema.yml`
- **Out-of-box tests** — `unique` and `not_null` applied in `schema.yml`

Test failures are stored in the database (`tests: +store_failures: true` in `dbt_project.yml`), queryable from `main_dbt_test__audit`.

## CI/CD

`.github/workflows/run-dbt-prod.yml` runs on every push/PR to `main`:
1. Installs dependencies from `requirements.txt`
2. Runs `dbt debug`, `dbt compile --target prod`, `dbt run --target prod`
3. Runs `dbt test --target prod`

The workflow sets `DBT_PROFILES_DIR` and `DBT_PROJECT_DIR` to `./nyc_parking_violations` so dbt commands run from the repo root in CI.

## Repository Notes

This is a LinkedIn Learning exercise-files repo. The `upstream` remote has one branch per course chapter (`chapter_01` … `chapter_11`), each a snapshot of the project at that point in the tutorial; `main` holds the final state. Don't assume `main` is the only branch of interest when the user references "a chapter" or "a lesson." The full walkthrough narrative (mirroring the chapter branches) is in `assets/tutorial_files/dbt_project_walkthrough.md`. Per `CONTRIBUTING.md`, this repo does not accept external pull requests.
