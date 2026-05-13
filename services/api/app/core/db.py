from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app.core.config import get_database_url


class DatabaseNotConfiguredError(RuntimeError):
    pass


@contextmanager
def get_db_connection():
    database_url = get_database_url()
    if not database_url:
        raise DatabaseNotConfiguredError(
            "DATABASE_URL or SUPABASE_DB_URL must be set.",
        )

    connection = psycopg.connect(database_url, row_factory=dict_row)
    try:
        yield connection
    finally:
        connection.close()

