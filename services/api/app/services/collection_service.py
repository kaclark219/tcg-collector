import psycopg
from psycopg.errors import ForeignKeyViolation, UndefinedTable

from app.core.db import DatabaseNotConfiguredError, get_db_connection
from app.data.mock_data import MOCK_COLLECTION_ENTRIES
from app.schemas.collection import CollectionEntry
from app.schemas.common import MutationResponse


class CollectionCreationError(ValueError):
    pass


class CollectionMoveError(ValueError):
    pass


class CollectionDeletionError(ValueError):
    pass


def _normalize_collection_entry(row: dict) -> CollectionEntry:
    return CollectionEntry(
        id=str(row["id"]),
        profile_id=str(row["profile_id"]),
        card_id=row["card_id"],
        binder_id=str(row["binder_id"]),
        variant=row["variant"],
        notes=row["notes"],
    )


def list_collection_entries(
    profile_id: str | None = None,
    binder_id: str | None = None,
) -> list[CollectionEntry]:
    if profile_id is None:
        return []

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                if binder_id:
                    cursor.execute(
                        """
                        select id, profile_id, card_id, binder_id, variant, notes
                        from public.collection_entries
                        where profile_id = %s and binder_id = %s
                        order by created_at desc
                        """,
                        (profile_id, binder_id),
                    )
                else:
                    cursor.execute(
                        """
                        select id, profile_id, card_id, binder_id, variant, notes
                        from public.collection_entries
                        where profile_id = %s
                        order by created_at desc
                        """,
                        (profile_id,),
                    )
                rows = cursor.fetchall()
            return [_normalize_collection_entry(row) for row in rows]
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
        return []


def get_collection_entry(entry_id: str) -> CollectionEntry | None:
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select id, profile_id, card_id, binder_id, variant, notes
                    from public.collection_entries
                    where id = %s
                    limit 1
                    """,
                    (entry_id,),
                )
                row = cursor.fetchone()
            if row is None:
                return None
            return _normalize_collection_entry(row)
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
        for entry in MOCK_COLLECTION_ENTRIES:
            if entry["id"] == entry_id:
                return CollectionEntry(
                    id=entry["id"],
                    profile_id=entry["profile_id"],
                    card_id=entry["card_id"],
                    binder_id=entry["binder_id"],
                    variant=entry["variant"],
                    notes=entry.get("notes"),
                )
        return None


def create_collection_entry(
    profile_id: str,
    card_id: str,
    binder_id: str,
    variant: str,
    notes: str | None,
) -> CollectionEntry:
    cleaned_variant = variant.strip() or "unknown"
    cleaned_notes = notes.strip() if notes else None
    if cleaned_notes == "":
        cleaned_notes = None

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    insert into public.collection_entries (
                      profile_id,
                      card_id,
                      binder_id,
                      variant,
                      notes
                    )
                    values (%s, %s, %s, %s, %s)
                    returning id, profile_id, card_id, binder_id, variant, notes
                    """,
                    (profile_id, card_id, binder_id, cleaned_variant, cleaned_notes),
                )
                row = cursor.fetchone()
            connection.commit()
    except ForeignKeyViolation as exc:
        raise CollectionCreationError("Invalid profile, card, or binder.") from exc
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error) as exc:
        raise CollectionCreationError("Unable to create collection entry right now.") from exc

    return _normalize_collection_entry(row)


def move_collection_entry(entry_id: str, binder_id: str) -> MutationResponse:
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    update public.collection_entries
                    set binder_id = %s
                    where id = %s
                    """,
                    (binder_id, entry_id),
                )
                updated_rows = cursor.rowcount
            connection.commit()
    except ForeignKeyViolation as exc:
        raise CollectionMoveError("Invalid binder for collection move.") from exc
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error) as exc:
        raise CollectionMoveError("Unable to move collection entry right now.") from exc

    if updated_rows == 0:
        raise CollectionMoveError("Collection entry not found.")

    return MutationResponse(
        success=True,
        message=f"Collection entry {entry_id} moved to binder {binder_id}.",
    )


def delete_collection_entry(entry_id: str) -> MutationResponse:
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    delete from public.collection_entries
                    where id = %s
                    """,
                    (entry_id,),
                )
                deleted_rows = cursor.rowcount
            connection.commit()
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error) as exc:
        raise CollectionDeletionError("Unable to delete collection entry right now.") from exc

    if deleted_rows == 0:
        raise CollectionDeletionError("Collection entry not found.")

    return MutationResponse(
        success=True,
        message=f"Collection entry {entry_id} deleted.",
    )
