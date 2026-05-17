from app.core.db import get_db_connection
from app.scripts.json_set_policy import SUPPLEMENTAL_SET_IDS


def main() -> None:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select c.set_id, c.set_name, count(*) as card_count
                from public.cards c
                where c.set_id = any(%s)
                group by c.set_id, c.set_name
                order by c.set_id
                """,
                (sorted(SUPPLEMENTAL_SET_IDS),),
            )
            target_sets = cursor.fetchall()

            if not target_sets:
                print("No supplemental sets found to delete.", flush=True)
                return

            cursor.execute(
                """
                select ce.card_id, c.set_id, c.set_name
                from public.collection_entries ce
                join public.cards c on c.id = ce.card_id
                where c.set_id = any(%s)
                order by c.set_id, ce.card_id
                limit 20
                """,
                (sorted(SUPPLEMENTAL_SET_IDS),),
            )
            referenced_cards = cursor.fetchall()

            if referenced_cards:
                print(
                    "Aborting cleanup because some supplemental cards are already in collection_entries.",
                    flush=True,
                )
                for row in referenced_cards:
                    print(
                        f"- referenced card {row['card_id']} from {row['set_name']} ({row['set_id']})",
                        flush=True,
                    )
                print(
                    "Move or delete those collection entries first, then rerun cleanup.",
                    flush=True,
                )
                return

            for row in target_sets:
                print(
                    f"- deleting {row['card_count']} cards from {row['set_name']} ({row['set_id']})",
                    flush=True,
                )

            cursor.execute(
                """
                delete from public.cards
                where set_id = any(%s)
                """,
                (sorted(SUPPLEMENTAL_SET_IDS),),
            )
        connection.commit()

    print("Supplemental set cleanup complete.", flush=True)


if __name__ == "__main__":
    main()
