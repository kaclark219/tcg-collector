from app.core.db import get_db_connection
from app.scripts.import_tcgdex_set import import_set


def find_sets_needing_repair() -> list[str]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select distinct set_id
                from public.cards
                where
                  set_id is not null
                  and (
                    image_url is null
                    or image_url not like '%%/high.png'
                  )
                order by set_id asc
                """
            )
            return [row["set_id"] for row in cursor.fetchall()]


def main() -> None:
    set_ids = find_sets_needing_repair()

    if not set_ids:
        print("No TCGdex image repairs needed.", flush=True)
        return

    print("Repairing TCGdex image URLs for sets:", ", ".join(set_ids), flush=True)
    for set_id in set_ids:
        stats = import_set(set_id=set_id, language="en")
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print("Done repairing image URLs.", flush=True)


if __name__ == "__main__":
    main()
