from app.database.connection import (
    get_sqlite_engine,
)

from app.database.metadata import (
    discover_schema,
)

from app.dq.engine import DQEngine


DB_PATH = r"./data/EDMTEST.db"


def main():

    print("=" * 70)
    print("DATA QUALITY POC")
    print("=" * 70)

    engine = get_sqlite_engine(DB_PATH)

    print("\nConnected to database successfully.\n")

    schema = discover_schema(engine)

    print("TABLES")
    print("-" * 70)

    for table, columns in schema.items():

        print(
            f"{table}: "
            f"{len(columns)} columns"
        )

    print("\nRunning DQ checks...\n")

    dq_engine = DQEngine(engine)

    findings = dq_engine.run()

    print(
        f"\nTotal findings: "
        f"{len(findings)}"
    )

    print("\nTOP FINDINGS")
    print("-" * 70)

    for finding in findings[:20]:

        print(
            f"[{finding['severity']}] "
            f"{finding['rule']} | "
            f"{finding['table']}.{finding['column']} | "
            f"{finding['details']}"
        )


if __name__ == "__main__":
    main()