from app.scripts.import_tcgdex_set import import_set

XY_SET_IDS = [
    "xy0",
    "xy1",
    "xy2",
    "xy3",
    "xy4",
    "xy5",
    "dc1",
    "xy6",
    "xy7",
    "xy8",
    "xy9",
    "g1",
    "xy10",
    "xy11",
    "xy12",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing XY series sets into public.cards...", flush=True)
    for set_id in XY_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. XY total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
