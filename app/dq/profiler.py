from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine


def profile_table(
    engine: Engine,
    table_name: str,
) -> dict[str, Any]:

    query = text(
        f'SELECT * FROM "{table_name}"'
    )

    df = pd.read_sql(query, engine)

    total_rows = len(df)

    columns = []

    for column in df.columns:

        series = df[column]

        null_count = int(series.isna().sum())

        distinct_count = int(series.nunique(dropna=True))

        duplicate_count = (
            total_rows - distinct_count
            if total_rows > 0
            else 0
        )

        columns.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "total_rows": total_rows,
                "null_count": null_count,
                "null_percentage": round(
                    (null_count / total_rows) * 100,
                    2,
                )
                if total_rows
                else 0,
                "distinct_count": distinct_count,
                "duplicate_count": duplicate_count,
            }
        )

    return {
        "table": table_name,
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "columns": columns,
    }