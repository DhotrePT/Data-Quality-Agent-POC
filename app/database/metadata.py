from typing import Any

from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def discover_schema(engine: Engine) -> dict[str, list[dict[str, Any]]]:
    """
    Discover tables and columns from the connected database.
    """

    inspector = inspect(engine)

    schema: dict[str, list[dict[str, Any]]] = {}

    for table_name in inspector.get_table_names():

        columns = []

        for column in inspector.get_columns(table_name):

            columns.append(
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column.get("nullable"),
                }
            )

        schema[table_name] = columns

    return schema