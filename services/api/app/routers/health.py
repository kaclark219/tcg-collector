from fastapi import APIRouter

from app.core.config import get_database_url
from app.core.db import DatabaseNotConfiguredError, get_db_connection

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict[str, str | bool]:
    database_configured = get_database_url() is not None
    database_reachable = False

    if database_configured:
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select 1")
                    cursor.fetchone()
                database_reachable = True
        except DatabaseNotConfiguredError:
            database_reachable = False
        except Exception:
            database_reachable = False

    return {
        "status": "ok",
        "database_configured": database_configured,
        "database_reachable": database_reachable,
    }
