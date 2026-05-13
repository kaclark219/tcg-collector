from app.scripts.import_tcgdex_set import import_set

SUN_AND_MOON_SET_IDS = [
    "sm1",
    "sm2",
    "sm3",
    "sm3.5",
    "sm4",
    "sm5",
    "sm6",
    "sm7",
    "sm7.5",
    "sm8",
    "sm9",
    "det1",
    "sm10",
    "sm11",
    "sm115",
    "sm12",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print("Importing Sun & Moon series sets into public.cards...", flush=True)
    for set_id in SUN_AND_MOON_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Sun & Moon total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
