from psycopg.errors import UndefinedTable
from psycopg.errors import ForeignKeyViolation, UniqueViolation

import psycopg

from app.core.db import DatabaseNotConfiguredError, get_db_connection
from app.data.mock_data import MOCK_BINDERS
from app.schemas.binders import Binder
from app.schemas.common import MutationResponse


class BinderCreationError(ValueError):
    pass


def list_binders(profile_id: str | None = None) -> list[Binder]:
    if profile_id is None:
        return [Binder(**binder) for binder in MOCK_BINDERS]

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select
                      b.id,
                      b.name,
                      b.description,
                      count(ce.id)::int as entry_count
                    from public.binders b
                    left join public.collection_entries ce
                      on ce.binder_id = b.id
                    where b.profile_id = %s
                    group by b.id, b.name, b.description, b.created_at
                    order by b.created_at asc
                    """,
                    (str(profile_id),),
                )
                rows = cursor.fetchall()
            return [
                Binder(
                    id=str(row["id"]),
                    name=row["name"],
                    description=row["description"],
                    entry_count=row["entry_count"],
                )
                for row in rows
            ]
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
        return [Binder(**binder) for binder in MOCK_BINDERS]


def get_binder(binder_id: str, profile_id: str | None = None) -> Binder | None:
    if profile_id is not None:
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        select
                          b.id,
                          b.name,
                          b.description,
                          count(ce.id)::int as entry_count
                        from public.binders b
                        left join public.collection_entries ce
                          on ce.binder_id = b.id
                        where b.id = %s and b.profile_id = %s
                        group by b.id, b.name, b.description
                        limit 1
                        """,
                        (binder_id, profile_id),
                    )
                    row = cursor.fetchone()
                if row is None:
                    return None
                return Binder(
                    id=str(row["id"]),
                    name=row["name"],
                    description=row["description"],
                    entry_count=row["entry_count"],
                )
        except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
            pass

    for binder in MOCK_BINDERS:
        if binder["id"] == binder_id:
            return Binder(**binder)
    return None


def create_binder(profile_id: str, name: str, description: str | None) -> Binder:
    cleaned_name = name.strip()
    if not cleaned_name:
        raise BinderCreationError("Binder name cannot be blank.")

    cleaned_description = description.strip() if description else None
    if cleaned_description == "":
        cleaned_description = None

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    insert into public.binders (profile_id, name, description, is_system)
                    values (%s, %s, %s, false)
                    returning id, name, description
                    """,
                    (profile_id, cleaned_name, cleaned_description),
                )
                row = cursor.fetchone()
            connection.commit()
    except UniqueViolation as exc:
        raise BinderCreationError("A binder with that name already exists.") from exc
    except ForeignKeyViolation as exc:
        raise BinderCreationError("Profile does not exist.") from exc
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error) as exc:
        raise BinderCreationError("Unable to create binder right now.") from exc

    return Binder(
        id=str(row["id"]),
        name=row["name"],
        description=row["description"],
        entry_count=0,
    )
