from app.scripts.import_tcgdex_set import import_set

SWORD_AND_SHIELD_SET_IDS = [
    "swsh1",
    "swsh2",
    "swsh3",
    "swsh3.5",
    "swsh4",
    "swsh4.5",
    "swsh5",
    "swsh6",
    "swsh7",
    "cel25",
    "swsh8",
    "swsh9",
    "swsh10",
    "swsh10.5",
    "swsh11",
    "swsh12",
    "swsh12.5",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing Sword & Shield series sets into public.cards...", flush=True)
    for set_id in SWORD_AND_SHIELD_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Sword & Shield total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
