from app.scripts.import_tcgdex_set import import_set

SCARLET_AND_VIOLET_SET_IDS = [
    "sv01",
    "sv02",
    "sv03",
    "sv03.5",
    "sv04",
    "sv04.5",
    "sv05",
    "sv06",
    "sv06.5",
    "sv07",
    "sv08",
    "sv08.5",
    "sv09",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing Scarlet & Violet series sets into public.cards...", flush=True)
    for set_id in SCARLET_AND_VIOLET_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Scarlet & Violet total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
