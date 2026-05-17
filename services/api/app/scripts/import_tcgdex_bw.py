from app.scripts.import_tcgdex_set import import_set

BLACK_AND_WHITE_SET_IDS = [
    "col1",
    "bw1",
    "bw2",
    "bw3",
    "bw4",
    "bw5",
    "bw6",
    "dv1",
    "bw7",
    "bw8",
    "bw9",
    "bw10",
    "bw11",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing Call of Legends and Black & White series sets into public.cards...", flush=True)
    for set_id in BLACK_AND_WHITE_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Call of Legends / Black & White total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
