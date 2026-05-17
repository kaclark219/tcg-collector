from dataclasses import dataclass
from pathlib import Path

from app.core.db import get_db_connection
from app.scripts.import_json_card_repo import (
    _iter_json_files,
    _load_cards_from_file,
    _pick_image_url,
    generate_card_id_aliases,
)


JSON_SOURCE_DIR = Path("import_sources/json_cards")


@dataclass
class RepairStats:
    cards_checked: int = 0
    json_matches: int = 0
    cards_updated: int = 0
    already_correct: int = 0
    missing_json_match: int = 0
    missing_json_image: int = 0


def build_json_image_index(source_dir: Path) -> dict[str, str]:
    image_by_card_id: dict[str, str] = {}

    for json_file in _iter_json_files(source_dir):
        for card in _load_cards_from_file(json_file):
            card_id = card.get("id")
            if not card_id:
                continue

            image_url = _pick_image_url(card)
            if image_url:
                for alias in generate_card_id_aliases(str(card_id)):
                    image_by_card_id[alias] = image_url

    return image_by_card_id


def main() -> None:
    source_dir = JSON_SOURCE_DIR
    if not source_dir.exists():
        raise FileNotFoundError(f"JSON source directory not found: {source_dir.resolve()}")

    image_by_card_id = build_json_image_index(source_dir)
    stats = RepairStats()

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select id, image_url
                from public.cards
                order by id
                """
            )
            cards = cursor.fetchall()

            for card in cards:
                stats.cards_checked += 1
                card_id = str(card["id"])
                current_image = card.get("image_url")
                json_image = image_by_card_id.get(card_id)

                if not json_image:
                    if card_id in image_by_card_id:
                        stats.missing_json_image += 1
                    else:
                        stats.missing_json_match += 1
                    continue

                stats.json_matches += 1

                if current_image == json_image:
                    stats.already_correct += 1
                    continue

                cursor.execute(
                    """
                    update public.cards
                    set image_url = %s
                    where id = %s
                    """,
                    (json_image, card_id),
                )
                stats.cards_updated += 1

        connection.commit()

    print(f"Checked {stats.cards_checked} cards.", flush=True)
    print(f"Matched {stats.json_matches} cards to local JSON.", flush=True)
    print(f"Updated {stats.cards_updated} image URLs.", flush=True)
    print(f"{stats.already_correct} image URLs were already correct.", flush=True)
    print(f"{stats.missing_json_match} cards had no matching JSON card ID.", flush=True)
    print(f"{stats.missing_json_image} matching JSON cards had no usable image URL.", flush=True)


if __name__ == "__main__":
    main()
