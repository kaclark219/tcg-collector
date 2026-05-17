from app.core.db import get_db_connection
from app.scripts.import_json_card_repo import card_id_priority, generate_card_id_aliases


def main() -> None:
    merged_count = 0

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select id, set_id, set_name, local_id, name, image_url
                from public.cards
                order by id
                """
            )
            cards = cursor.fetchall()

            card_by_id = {row["id"]: row for row in cards}
            merge_pairs: list[tuple[str, str]] = []

            for row in cards:
                source_id = row["id"]
                matches = [
                    alias
                    for alias in generate_card_id_aliases(source_id)
                    if alias in card_by_id
                ]
                if len(matches) < 2:
                    continue

                target_id = min(matches, key=card_id_priority)
                if target_id != source_id:
                    merge_pairs.append((source_id, target_id))

            seen_sources: set[str] = set()
            for source_id, target_id in merge_pairs:
                if source_id in seen_sources:
                    continue
                seen_sources.add(source_id)

                cursor.execute(
                    """
                    update public.collection_entries
                    set card_id = %s
                    where card_id = %s
                    """,
                    (target_id, source_id),
                )

                cursor.execute(
                    """
                    update public.cards as target
                    set
                      image_url = coalesce(target.image_url, source.image_url),
                      updated_at_source = coalesce(target.updated_at_source, source.updated_at_source)
                    from public.cards as source
                    where target.id = %s
                      and source.id = %s
                    """,
                    (target_id, source_id),
                )

                cursor.execute(
                    """
                    delete from public.cards
                    where id = %s
                    """,
                    (source_id,),
                )
                merged_count += 1
                print(f"- merged {source_id} -> {target_id}", flush=True)

        connection.commit()

    print(f"Done. Merged {merged_count} aliased card rows.", flush=True)


if __name__ == "__main__":
    main()
