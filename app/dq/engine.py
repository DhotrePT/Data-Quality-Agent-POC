from typing import Any

import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from app.dq.rules import (
    check_duplicates,
    check_nulls,
    check_wo_number_uniqueness,
    check_work_order_dates,
    check_status_date_consistency,
)

SYSTEM_TABLES = {"incidents"}


class DQEngine:

    def __init__(self, engine: Engine):
        self.engine = engine

    def run(self) -> list[dict[str, Any]]:

        inspector = inspect(self.engine)

        tables = inspector.get_table_names()

        all_findings = []

        for table_name in tables:

            if table_name.lower() in SYSTEM_TABLES:
                continue

            print(f"Scanning table: {table_name}")

            query = text(f'SELECT * FROM "{table_name}"')

            df = pd.read_sql(query, self.engine)

            # Generic rules
            all_findings.extend(check_nulls(df, table_name))
            all_findings.extend(check_duplicates(df, table_name))
            all_findings.extend(check_wo_number_uniqueness(df, table_name))
            all_findings.extend(check_work_order_dates(df, table_name))
            all_findings.extend(check_status_date_consistency(df, table_name))

        return all_findings