from app.scripts.import_tcgdex_set import import_set

WOTC_SET_IDS = [
    "base1",
    "base2",
    "base3",
    "base4",
    "base5",
    "gym1",
    "gym2",
    "neo1",
    "neo2",
    "neo3",
    "neo4",
    "lc",
    "ecard1",
    "ecard2",
    "ecard3",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print(
        "Importing Original, Neo, Legendary Collection, and e-Card series sets into public.cards...",
        flush=True,
    )
    for set_id in WOTC_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Early-era total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
