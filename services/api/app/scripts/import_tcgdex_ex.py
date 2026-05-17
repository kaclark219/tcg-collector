from app.scripts.import_tcgdex_set import import_set

EX_SET_IDS = [
    "ex1",
    "ex2",
    "ex3",
    "ex4",
    "ex5",
    "ex6",
    "ex7",
    "ex8",
    "ex9",
    "ex10",
    "ex11",
    "ex12",
    "ex13",
    "ex14",
    "ex15",
    "ex16",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing EX series sets into public.cards...", flush=True)
    for set_id in EX_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. EX total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
