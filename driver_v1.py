# ============================================================
# SETUP INSTRUCTIONS
# ============================================================
#
# Setup:
#   pip install duckdb
#
# Requires Python 3.8+ and duckdb
# ============================================================

from dataclasses import dataclass
from typing import Callable, Dict, List

import duckdb

# ============================================================
# DATABASE SETUP (do not modify)
# ============================================================

def create_database() -> duckdb.DuckDBPyConnection:
    """Create a file-backed DuckDB database with mock DoorDash delivery data."""
    db = duckdb.connect("driver_v1.duckdb")

    db.execute("""
        CREATE TABLE raw_deliveries (
            delivery_id INTEGER,
            store_id INTEGER,
            dasher_id INTEGER,
            consumer_id INTEGER,
            subtotal DOUBLE,
            delivery_fee DOUBLE,
            tip DOUBLE,
            delivery_status VARCHAR,
            estimated_delivery_at TIMESTAMP,
            actual_delivery_at TIMESTAMP,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)

    db.execute("""
        INSERT INTO raw_deliveries VALUES
        (5001, 10, 201, 501, 25.50, 3.99, 5.00, 'completed', '2024-01-15 12:30:00', '2024-01-15 12:15:00', '2024-01-15 11:30:00', '2024-01-15 12:15:00'),
        (5002, 10, 202, 502, 18.75, 4.99, 3.00, 'completed', '2024-01-15 13:00:00', '2024-01-15 13:42:00', '2024-01-15 12:15:00', '2024-01-15 13:42:00'),
        (5003, 20, 203, 503, 42.00, 2.99, 8.00, 'completed', '2024-01-15 14:00:00', '2024-01-15 13:50:00', '2024-01-15 13:00:00', '2024-01-15 13:50:00'),
        (5004, 20, 204, 504, 15.00, 3.99, 0.00, 'in_progress', '2024-01-15 15:00:00', NULL, '2024-01-15 14:30:00', '2024-01-15 14:30:00'),
        (5005, 30, 205, 505, 33.25, 5.99, 6.00, 'completed', '2024-01-15 16:00:00', '2024-01-15 16:22:00', '2024-01-15 15:30:00', '2024-01-15 16:22:00'),
        (5006, 30, 206, 506, 22.00, 3.99, 4.00, 'canceled', '2024-01-15 17:00:00', NULL, '2024-01-15 16:30:00', '2024-01-15 17:00:00'),
        (5007, 10, 207, 507, 55.00, 2.99, 10.00, 'completed', '2024-01-15 18:00:00', '2024-01-16 18:00:00', '2024-01-15 17:00:00', '2024-01-15 18:00:00'),
        (5008, 20, 208, 508, 29.99, 4.99, 5.00, 'completed', '2024-01-16 12:30:00', '2024-01-16 12:45:00', '2024-01-16 11:30:00', '2024-01-16 12:45:00'),
        (5009, 30, 209, 509, 12.50, 3.99, 2.00, 'completed', '2024-01-16 14:00:00', '2024-01-16 14:48:00', '2024-01-16 13:00:00', '2024-01-16 13:48:00'),
        (5010, 10, 210, 510, 38.00, 4.99, 7.00, 'completed', '2024-01-16 16:00:00', NULL, '2024-01-16 15:55:00', '2024-01-16 15:55:00'),
        (5011, 40, 211, 511, 20.00, 3.99, 3.00, 'completed', '2024-01-15 19:00:00', '2024-01-15 18:55:00', '2024-01-15 18:00:00', '2024-01-15 18:55:00'),
        (5012, 50, 212, 512, 15.00, 3.99, 2.00, 'completed', '2024-01-15 20:00:00', '2024-01-13 19:58:00', '2024-01-15 19:00:00', '2024-01-15 19:00:00'),
        (5013, 60, 213, 513, 48.00, 4.99, 9.00, 'completed', '2024-01-15 13:00:00', '2024-01-15 12:50:00', '2024-01-15 12:00:00', '2024-01-15 12:50:00'),
        (5014, 60, 214, 514, 22.50, 3.99, 4.00, 'completed', '2024-01-15 18:00:00', '2024-01-15 18:25:00', '2024-01-15 17:00:00', '2024-01-15 18:25:00'),
        (5015, 70, 215, 515, 17.00, 2.99, 4.00, 'completed', '2024-01-16 19:00:00', '2024-01-16 18:00:00', '2024-01-16 17:00:00', '2024-01-16 19:20:00'),
        (5016, 20, 216, 516, 27.50, 4.99, 5.00, 'completed', '2024-01-17 12:00:00', '2024-01-17 12:10:00', '2024-01-17 11:00:00', '2024-01-17 12:10:00'),
        (5017, 20, 217, 517, 31.00, 3.99, 6.00, 'completed', '2024-01-17 13:00:00', '2024-01-17 12:55:00', '2024-01-17 12:00:00', '2024-01-17 12:55:00'),
        (5018, 60, 218, 518, 40.00, 4.99, 8.00, 'completed', '2024-01-17 14:00:00', '2024-01-17 13:52:00', '2024-01-17 13:52:00', '2024-01-17 13:52:00'),
        (5019, 70, 219, 519, 14.00, 2.99, 4.00, 'completed', '2024-01-17 15:00:00', '2024-01-17 15:00:00', '2024-01-17 14:00:00', '2024-01-17 15:00:00'),
        (5020, 20, 220, 520, 19.50, 3.99, 3.00, 'completed', '2024-01-16 17:00:00', '2024-01-16 16:57:00', '2024-01-16 16:00:00', '2024-01-16 16:57:00'),
        (5021, 20, 221, 521, 26.00, 4.99, 4.00, 'completed', '2024-01-17 18:00:00', '2024-01-17 17:00:00', '2024-01-17 17:00:00', '2024-01-17 17:00:00'),
        (5022, 40, 222, 522, 12.00, 3.99, 1.00, 'in_progress', '2024-01-16 20:00:00', NULL, '2024-01-16 19:55:00', '2024-01-16 19:55:00'),
        (5008, 20, 208, 508, 29.99, 4.99, 5.00, 'completed', '2024-01-16 12:30:00', '2024-01-16 12:48:00', '2024-01-16 11:30:00', '2024-01-16 12:50:00'),
        (5024, 10, 224, 524, 18.00, 4.99, 3.00, 'Completed', '2024-01-17 13:00:00', '2024-01-17 13:05:00', '2024-01-17 12:00:00', '2024-01-17 13:05:00'),
        (5025, 80, 225, 525, 22.00, 4.99, 4.00, 'completed', '2024-01-16 18:00:00', '2024-01-15 15:00:00', '2024-01-15 15:00:00', '2024-01-15 15:53:00'),
        (5026, 80, 226, 526, 35.50, 3.99, 7.00, 'completed', '2024-01-15 19:30:00', '2024-01-15 19:48:00', '2024-01-15 18:30:00', '2024-01-15 19:48:00'),
        (5027, 80, 227, 527, 28.00, 4.99, 6.00, 'completed', '2024-01-16 12:00:00', '2024-01-16 12:05:00', '2024-01-16 11:00:00', '2024-01-16 12:05:00'),
        (5028, 80, 228, 528, 19.50, 3.99, 3.00, 'completed', '2024-01-16 14:30:00', '2024-01-17 14:25:00', '2024-01-17 13:30:00', '2024-01-17 14:25:00')
    """)

    db.execute("""
        CREATE TABLE raw_stores (
            store_id INTEGER,
            store_name VARCHAR,
            business_id INTEGER,
            business_name VARCHAR,
            business_type VARCHAR,
            submarket_id INTEGER,
            is_active_store BOOLEAN,
            is_test_store BOOLEAN,
            onboarded_at TIMESTAMP,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)

    db.execute("""
        INSERT INTO raw_stores VALUES
        (10, 'Pizza Palace - Market St', 100, 'Pizza Palace', 'restaurant', 1, true, false, '2023-09-01 00:00:00', '2023-09-01 00:00:00', '2024-01-01 00:00:00'),
        (20, 'Burger Barn - Main', 200, 'Burger Barn', 'restaurant', 1, true, false, '2023-11-01 00:00:00', '2023-11-01 00:00:00', '2024-01-01 00:00:00'),
        (30, 'Quick Mart - 5th Ave', 300, 'Quick Mart', 'convenience', 2, true, false, '2024-01-01 00:00:00', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
        (40, 'QA Test Kitchen', 400, 'QA Test', 'restaurant', 1, true, true, '2023-06-01 00:00:00', '2023-06-01 00:00:00', '2024-01-01 00:00:00'),
        (50, 'Closed Diner', 500, 'Old Diner', 'restaurant', 2, false, false, '2023-03-01 00:00:00', '2023-03-01 00:00:00', '2024-01-10 00:00:00'),
        (60, 'Sushi Spot - Downtown', 600, 'Sushi Spot', 'restaurant', 2, true, false, '2023-08-15 00:00:00', '2023-08-15 00:00:00', '2024-01-01 00:00:00'),
        (70, 'Taco Truck - Plaza', 700, 'Taco Truck', 'restaurant', 3, true, false, '2024-01-08 00:00:00', '2024-01-08 00:00:00', '2024-01-01 00:00:00'),
        (80, 'Slice House - Mission', 800, 'Slice House', 'restaurant', 1, true, false, '2023-10-01 00:00:00', '2023-10-01 00:00:00', '2024-01-16 00:00:00')
    """)

    return db


# ============================================================
# (candidate fills in from here)
# ============================================================

SQL_TRANSFORMS: Dict[str, dict] = {
    # ---------------- SILVER ----------------
    "silver_deliveries": {
        "depends_on": [],
        "sql": """
            SELECT
                delivery_id,
                store_id,
                dasher_id,
                consumer_id,
                subtotal,
                delivery_fee,
                tip,
                LOWER(delivery_status) AS delivery_status,
                estimated_delivery_at,
                actual_delivery_at,
                created_at,
                updated_at
            FROM raw_deliveries
            -- Dedup rule (confirmed): keep the row with the latest
            -- actual_delivery_at per delivery_id. NULLS LAST so an
            -- in-progress duplicate never wins over a resolved one.
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY delivery_id
                ORDER BY actual_delivery_at DESC NULLS LAST, updated_at DESC
            ) = 1
        """,
    },
    "silver_stores": {
        "depends_on": [],
        "sql": """
            SELECT
                store_id,
                store_name,
                business_id,
                business_name,
                business_type,
                submarket_id,
                is_active_store,
                is_test_store,
                onboarded_at,
                created_at,
                updated_at
            FROM raw_stores
            -- Confirmed: exclude QA/test stores from business metrics.
            WHERE is_test_store = false
        """,
    },
    # ---------------- GOLD: DIMENSION ----------------
    "dim_store": {
        "depends_on": ["silver_stores"],
        "sql": """
            SELECT
                store_id,
                store_name,
                business_id,
                business_name,
                business_type,
                submarket_id,
                is_active_store,
                onboarded_at
            FROM silver_stores
        """,
    },
    # ---------------- GOLD: FACT ----------------
    # Grain: one row per delivery. dasher_id/consumer_id are kept as
    # degenerate dimensions directly on the fact table -- there is no
    # raw_dashers/raw_consumers table to build real dimensions from.
    "fact_deliveries": {
        "depends_on": ["silver_deliveries", "dim_store"],
        "sql": """
            SELECT
                d.delivery_id,
                d.store_id,
                d.dasher_id,
                d.consumer_id,
                d.subtotal,
                d.delivery_fee,
                d.tip,
                d.delivery_status,
                -- Confirmed definition: complete = actual equals estimated.
                -- COALESCE handles NULL actual_delivery_at (in_progress/
                -- canceled orders) as "not complete" rather than NULL.
                COALESCE(d.actual_delivery_at = d.estimated_delivery_at, false)
                    AS is_complete_delivery,
                d.estimated_delivery_at,
                d.actual_delivery_at,
                d.created_at,
                d.updated_at
            FROM silver_deliveries d
            -- INNER JOIN: deliveries at excluded test stores drop out here,
            -- consistent with excluding test stores from business metrics.
            -- Confirmed: all delivery_status values are kept (completed,
            -- canceled, in_progress) so Q3's drill-down has something to show.
            INNER JOIN dim_store s ON d.store_id = s.store_id
        """,
    },
}

FINAL_OUTPUT_TABLE: str = "fact_deliveries"

# Data-quality checks, run after the transform DAG. Same run_task()
# helper, just kind="check" -- 0 returned rows means the check passed.
CHECKS: Dict[str, dict] = {
    "silver_deliveries_unique": {
        "sql": """
            SELECT delivery_id, COUNT(*) AS n
            FROM silver_deliveries
            GROUP BY delivery_id
            HAVING COUNT(*) > 1
        """
    },
    "silver_deliveries_not_null": {
        "sql": """
            SELECT delivery_id
            FROM silver_deliveries
            WHERE delivery_id IS NULL OR store_id IS NULL OR delivery_status IS NULL
        """
    },
    "fact_deliveries_amounts_non_negative": {
        "sql": """
            SELECT delivery_id
            FROM fact_deliveries
            WHERE subtotal < 0 OR delivery_fee < 0 OR tip < 0
        """
    },
    "fact_store_referential_integrity": {
        "sql": """
            SELECT f.delivery_id
            FROM fact_deliveries f
            LEFT JOIN dim_store s ON f.store_id = s.store_id
            WHERE s.store_id IS NULL
        """
    },
    "dedup_reconciliation": {
        "sql": """
            SELECT 'mismatch' AS reason
            WHERE (SELECT COUNT(DISTINCT delivery_id) FROM raw_deliveries)
                <> (SELECT COUNT(*) FROM silver_deliveries)
        """
    },
}


def resolve_execution_order(transforms: Dict[str, dict]) -> List[str]:
    """Return the order in which transforms should run (topological sort)."""
    state: Dict[str, str] = {}
    order: List[str] = []

    def visit(name: str, path: List[str]) -> None:
        if state.get(name) == "done":
            return
        if state.get(name) == "visiting":
            raise ValueError(f"Circular dependency: {' -> '.join(path + [name])}")
        if name not in transforms:
            raise ValueError(f"Unknown transform referenced: {name!r}")

        state[name] = "visiting"
        for dep in transforms[name].get("depends_on", []):
            visit(dep, path + [name])
        state[name] = "done"
        order.append(name)

    for name in transforms:
        visit(name, [])

    return order


def print_business_answers(db: duckdb.DuckDBPyConnection) -> None:
    """Ad-hoc queries against the gold layer -- not materialized tables,
    per the confirmed plan. fact_deliveries + dim_store answer all four
    business questions directly."""

    print("\n1) Deliveries per store:")
    for row in db.execute("""
        SELECT s.store_name, COUNT(*) AS delivery_count
        FROM fact_deliveries f
        JOIN dim_store s ON f.store_id = s.store_id
        GROUP BY s.store_name
        ORDER BY delivery_count DESC
    """).fetchall():
        print(f"   {row[0]}: {row[1]}")

    print("\n2) Deliveries per dasher:")
    for row in db.execute("""
        SELECT dasher_id, COUNT(*) AS delivery_count
        FROM fact_deliveries
        GROUP BY dasher_id
        ORDER BY delivery_count DESC
    """).fetchall():
        print(f"   dasher {row[0]}: {row[1]}")

    print("\n3) Deliveries by status:")
    for row in db.execute("""
        SELECT delivery_status, COUNT(*) AS delivery_count
        FROM fact_deliveries
        GROUP BY delivery_status
        ORDER BY delivery_count DESC
    """).fetchall():
        print(f"   {row[0]}: {row[1]}")

    print("\n4) Complete deliveries (actual_delivery_at = estimated_delivery_at):")
    for row in db.execute("""
        SELECT is_complete_delivery, COUNT(*) AS delivery_count
        FROM fact_deliveries
        GROUP BY is_complete_delivery
    """).fetchall():
        label = "complete" if row[0] else "not complete"
        print(f"   {label}: {row[1]}")


def main():
    db = create_database()

    print("Running pipeline...")
    for name in resolve_execution_order(SQL_TRANSFORMS):
        result = run_task(db, "transform", name, SQL_TRANSFORMS[name]["sql"])
        print(f"  {result['name']}: {result['row_count']} rows")

    print("\nRunning data quality checks:")
    for name, spec in CHECKS.items():
        result = run_task(db, "check", name, spec["sql"])
        status = "PASS" if result["passed"] else f"FAIL ({result['bad_row_count']} bad rows)"
        print(f"  {status}: {result['name']}")

    print_business_answers(db)

    print("\nRunning tests:")
    run_tests(_get_test_cases(db))


# ============================================================
# FRAMEWORK (do not modify)
# ============================================================

@dataclass
class TestCase:
    """A single test: a name and a zero-arg check that raises on failure."""
    name: str
    check: Callable[[], None]


def run_task(db: duckdb.DuckDBPyConnection, kind: str, name: str, sql: str) -> dict:
    """Run a single SQL task.

    kind="transform":  runs `CREATE OR REPLACE TABLE {name} AS ({sql})`
                        Returns {kind, name, row_count}.
    kind="check":       runs {sql} as a SELECT; 0 returned rows = passed.
                        Returns {kind, name, passed, bad_row_count}.
    """
    if kind == "transform":
        db.execute(f"CREATE OR REPLACE TABLE {name} AS ({sql})")
        row_count = db.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        return {"kind": kind, "name": name, "row_count": row_count}
    if kind == "check":
        bad_rows = db.execute(sql).fetchall()
        return {
            "kind": kind,
            "name": name,
            "passed": len(bad_rows) == 0,
            "bad_row_count": len(bad_rows),
        }
    raise ValueError(f"Unknown task kind: {kind!r}")


def run_tests(test_cases: List[TestCase]) -> int:
    """Run test cases and print a summary. Returns the number of failures."""
    passed = 0
    failed = 0
    for tc in test_cases:
        try:
            tc.check()
            print(f"  PASS: {tc.name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {tc.name}")
            print(f"        {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {tc.name}")
            print(f"        {type(e).__name__}: {e}")
            failed += 1
    total = len(test_cases)
    print(f"\nResults: {passed} passed, {failed} failed out of {total} tests")
    return failed


# ============================================================
# TESTS (do not modify)
# ============================================================

def _get_test_cases(db: duckdb.DuckDBPyConnection) -> List[TestCase]:
    return [
        TestCase(
            name="execution order respects declared dependencies",
            check=_assert_execution_order,
        ),
        TestCase(
            name="final output table is populated",
            check=lambda: _assert_final_table_has_rows(db),
        ),
    ]


def _assert_execution_order():
    if not SQL_TRANSFORMS:
        raise AssertionError("SQL_TRANSFORMS is empty -- no transforms declared")
    order = resolve_execution_order(SQL_TRANSFORMS)
    assert set(order) == set(SQL_TRANSFORMS), (
        f"resolve_execution_order is missing transforms: "
        f"{sorted(set(SQL_TRANSFORMS) - set(order))}"
    )
    seen = set()
    for tid in order:
        for dep in SQL_TRANSFORMS[tid].get("depends_on", []):
            assert dep in seen, (
                f"transform {tid!r} ran before its dependency {dep!r}"
            )
        seen.add(tid)


def _assert_final_table_has_rows(db: duckdb.DuckDBPyConnection):
    assert FINAL_OUTPUT_TABLE, (
        "FINAL_OUTPUT_TABLE is not set in interview.py"
    )
    row = db.execute(f"SELECT COUNT(*) FROM {FINAL_OUTPUT_TABLE}").fetchone()
    assert row[0] > 0, f"final output table {FINAL_OUTPUT_TABLE!r} is empty"


if __name__ == "__main__":
    main()