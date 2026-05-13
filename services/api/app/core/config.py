import os
from pathlib import Path

from dotenv import load_dotenv


def _load_env_files() -> None:
    # Load a repo-level .env first, then let a service-specific .env override it.
    current_file = Path(__file__).resolve()
    repo_root = current_file.parents[4]
    service_root = current_file.parents[2]

    load_dotenv(repo_root / ".env")
    load_dotenv(service_root / ".env", override=True)


_load_env_files()


def get_database_url() -> str | None:
    # Prefer a generic DATABASE_URL, but allow a Supabase-specific fallback
    # while the project is still being wired up.
    return os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")

