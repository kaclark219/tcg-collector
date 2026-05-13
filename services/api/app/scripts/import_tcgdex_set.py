import argparse
from dataclasses import dataclass

from tcgdexsdk import TCGdex
from tcgdexsdk.enums import Extension, Quality

from app.core.db import get_db_connection


@dataclass
class ImportStats:
    set_id: str
    set_name: str
    cards_seen: int = 0
    cards_upserted: int = 0


def _card_image_url(card) -> str | None:
    if not getattr(card, "image", None):
        return None

    get_image_url = getattr(card, "get_image_url", None)
    if callable(get_image_url):
        return str(get_image_url(Quality.HIGH, Extension.PNG))

    image_value = getattr(card, "image", None)
    return str(image_value) if image_value else None


def upsert_card(cursor, card) -> None:
    cursor.execute(
        """
        insert into public.cards (
          id,
          local_id,
          name,
          image_url,
          category,
          illustrator,
          rarity,
          set_id,
          set_name,
          variant_normal,
          variant_reverse,
          variant_holo,
          variant_first_edition,
          variant_w_promo,
          updated_at_source
        )
        values (
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        on conflict (id) do update
        set
          local_id = excluded.local_id,
          name = excluded.name,
          image_url = excluded.image_url,
          category = excluded.category,
          illustrator = excluded.illustrator,
          rarity = excluded.rarity,
          set_id = excluded.set_id,
          set_name = excluded.set_name,
          variant_normal = excluded.variant_normal,
          variant_reverse = excluded.variant_reverse,
          variant_holo = excluded.variant_holo,
          variant_first_edition = excluded.variant_first_edition,
          variant_w_promo = excluded.variant_w_promo,
          updated_at_source = excluded.updated_at_source
        """,
        (
            card.id,
            str(getattr(card, "localId", "")) or None,
            card.name,
            _card_image_url(card),
            getattr(card, "category", None),
            getattr(card, "illustrator", None),
            getattr(card, "rarity", None),
            card.set.id if getattr(card, "set", None) else None,
            card.set.name if getattr(card, "set", None) else None,
            bool(getattr(card.variants, "normal", False)) if getattr(card, "variants", None) else False,
            bool(getattr(card.variants, "reverse", False)) if getattr(card, "variants", None) else False,
            bool(getattr(card.variants, "holo", False)) if getattr(card, "variants", None) else False,
            bool(getattr(card.variants, "firstEdition", False)) if getattr(card, "variants", None) else False,
            bool(getattr(card.variants, "wPromo", False)) if getattr(card, "variants", None) else False,
            getattr(card, "updated", None),
        ),
    )


def import_set(set_id: str, language: str) -> ImportStats:
    sdk = TCGdex(language)
    set_data = sdk.set.getSync(set_id)

    if not set_data:
        raise RuntimeError(f"Set '{set_id}' was not found in TCGdex.")

    stats = ImportStats(
        set_id=set_id,
        set_name=getattr(set_data, "name", set_id),
    )

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            for card_brief in getattr(set_data, "cards", []) or []:
                full_card = sdk.card.getSync(card_brief.id)
                if not full_card:
                    continue
                stats.cards_seen += 1
                upsert_card(cursor, full_card)
                stats.cards_upserted += 1

        connection.commit()

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import one TCGdex set into public.cards.",
    )
    parser.add_argument(
        "--set-id",
        default="swsh3",
        help="TCGdex set ID to import. Use 'swsh3' for Darkness Ablaze.",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="TCGdex language code, default: en",
    )
    args = parser.parse_args()

    stats = import_set(args.set_id, args.language)
    print(
        f"Imported set {stats.set_name} ({stats.set_id}): "
        f"{stats.cards_upserted}/{stats.cards_seen} cards upserted."
    )


if __name__ == "__main__":
    main()
