from app.scripts.import_tcgdex_set import import_set

DP_PL_HGSS_SET_IDS = [
    "dp1",
    "dp2",
    "dp3",
    "dp4",
    "dp5",
    "dp6",
    "dp7",
    "pl1",
    "pl2",
    "pl3",
    "pl4",
    "hgss1",
    "hgss2",
    "hgss3",
    "hgss4",
]


def main() -> None:
    total_upserted = 0
    total_seen = 0

    print(
        "Importing Diamond & Pearl, Platinum, and HGSS series sets into public.cards...",
        flush=True,
    )
    for set_id in DP_PL_HGSS_SET_IDS:
        stats = import_set(set_id=set_id, language="en")
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {stats.set_name} ({stats.set_id}): "
            f"{stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. DP / Platinum / HGSS total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
