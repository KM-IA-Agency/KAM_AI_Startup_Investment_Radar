from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.sqlite_migrations import ensure_sqlite_schema_compatibility

load_dotenv()

DEFAULT_DATABASE_URL = "sqlite:///startup_radar_local.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine(database_url: str | None = None) -> Engine:
    url = database_url or get_database_url()
    return create_engine(url, future=True)


def execute_sql_file(sql_path: str | Path = "sql/schema.sql", database_url: str | None = None) -> None:
    engine = get_engine(database_url)
    sql_path = Path(sql_path)
    sql = sql_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))

    ensure_sqlite_schema_compatibility(engine)


if __name__ == "__main__":
    print(get_database_url())
