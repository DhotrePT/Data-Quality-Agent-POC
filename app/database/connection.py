from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_sqlite_engine(db_path: str) -> Engine:
    """
    Create a SQLAlchemy engine for SQLite.

    This function intentionally hides the database-specific
    connection details from the rest of the application.
    Later, we can add SQL Server without changing the DQ engine.
    """

    path = Path(db_path).resolve()

    if not path.exists():
        raise FileNotFoundError(
            f"Database not found: {path}"
        )

    return create_engine(
        f"sqlite:///{path}",
        echo=False,
    )