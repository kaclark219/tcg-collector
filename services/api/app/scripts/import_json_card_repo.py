import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.core.db import get_db_connection
from app.scripts.json_set_policy import SUPPLEMENTAL_SET_IDS


@dataclass
class ImportStats:
    source_path: str
    cards_seen: int = 0
    cards_upserted: int = 0


LOCAL_SET_NAME_OVERRIDES = {
    "base1": "Base Set",
    "base2": "Jungle",
    "base3": "Fossil",
    "base4": "Base Set 2",
    "base5": "Team Rocket",
    "base6": "Legendary Collection",
    "bp": "Best of Game",
    "bw1": "Black & White",
    "bw2": "Emerging Powers",
    "bw3": "Noble Victories",
    "bw4": "Next Destinies",
    "bw5": "Dark Explorers",
    "bw6": "Dragons Exalted",
    "bw7": "Boundaries Crossed",
    "bw8": "Plasma Storm",
    "bw9": "Plasma Freeze",
    "bw10": "Plasma Blast",
    "bw11": "Legendary Treasures",
    "cel25": "Celebrations",
    "cel25c": "Celebrations: Classic Collection",
    "col1": "Call of Legends",
    "dc1": "Double Crisis",
    "det1": "Detective Pikachu",
    "dp1": "Diamond & Pearl",
    "dp2": "Mysterious Treasures",
    "dp3": "Secret Wonders",
    "dp4": "Great Encounters",
    "dp5": "Majestic Dawn",
    "dp6": "Legends Awakened",
    "dp7": "Stormfront",
    "dv1": "Dragon Vault",
    "ecard1": "Expedition Base Set",
    "ecard2": "Aquapolis",
    "ecard3": "Skyridge",
    "ex1": "Ruby & Sapphire",
    "ex2": "Sandstorm",
    "ex3": "Dragon",
    "ex4": "Team Magma vs Team Aqua",
    "ex5": "Hidden Legends",
    "ex6": "FireRed & LeafGreen",
    "ex7": "Team Rocket Returns",
    "ex8": "Deoxys",
    "ex9": "Emerald",
    "ex10": "Unseen Forces",
    "ex11": "Delta Species",
    "ex12": "Legend Maker",
    "ex13": "Holon Phantoms",
    "ex14": "Crystal Guardians",
    "ex15": "Dragon Frontiers",
    "ex16": "Power Keepers",
    "g1": "Generations",
    "gym1": "Gym Heroes",
    "gym2": "Gym Challenge",
    "hgss1": "HeartGold SoulSilver",
    "hgss2": "Unleashed",
    "hgss3": "Undaunted",
    "hgss4": "Triumphant",
    "lc": "Legendary Collection",
    "mcd11": "McDonald's Collection 2011",
    "mcd12": "McDonald's Collection 2012",
    "mcd14": "McDonald's Collection 2014",
    "mcd15": "McDonald's Collection 2015",
    "mcd16": "McDonald's Collection 2016",
    "mcd17": "McDonald's Collection 2017",
    "mcd18": "McDonald's Collection 2018",
    "mcd19": "McDonald's Collection 2019",
    "mcd21": "McDonald's Collection 2021",
    "mcd22": "McDonald's Collection 2022",
    "me1": "Mega Evolution",
    "me2": "Mega Evolution—Phantasmal Flames",
    "me2pt5": "Mega Evolution—Ascended Heroes",
    "me3": "Mega Evolution—Perfect Order",
    "neo1": "Neo Genesis",
    "neo2": "Neo Discovery",
    "neo3": "Neo Revelation",
    "neo4": "Neo Destiny",
    "np": "Nintendo Promos",
    "pgo": "Pokémon GO",
    "pl1": "Platinum",
    "pl2": "Rising Rivals",
    "pl3": "Supreme Victors",
    "pl4": "Arceus",
    "pop1": "POP Series 1",
    "pop2": "POP Series 2",
    "pop3": "POP Series 3",
    "pop4": "POP Series 4",
    "pop5": "POP Series 5",
    "pop6": "POP Series 6",
    "pop7": "POP Series 7",
    "pop8": "POP Series 8",
    "pop9": "POP Series 9",
    "rsv10pt5": "Scarlet & Violet—White Flare",
    "si1": "Southern Islands",
    "sm1": "Sun & Moon",
    "sm2": "Guardians Rising",
    "sm3": "Burning Shadows",
    "sm35": "Shining Legends",
    "sm4": "Crimson Invasion",
    "sm5": "Ultra Prism",
    "sm6": "Forbidden Light",
    "sm7": "Celestial Storm",
    "sm75": "Dragon Majesty",
    "sm8": "Lost Thunder",
    "sm9": "Team Up",
    "sm10": "Unbroken Bonds",
    "sm11": "Unified Minds",
    "sm115": "Hidden Fates",
    "sm12": "Cosmic Eclipse",
    "sv1": "Scarlet & Violet",
    "sv2": "Paldea Evolved",
    "sv3": "Obsidian Flames",
    "sv3pt5": "151",
    "sv4": "Paradox Rift",
    "sv4pt5": "Paldean Fates",
    "sv5": "Temporal Forces",
    "sv6": "Twilight Masquerade",
    "sv6pt5": "Shrouded Fable",
    "sv7": "Stellar Crown",
    "sv8": "Surging Sparks",
    "sv8pt5": "Prismatic Evolutions",
    "sv9": "Journey Together",
    "sv10": "Destined Rivals",
    "swsh1": "Sword & Shield",
    "swsh2": "Rebel Clash",
    "swsh3": "Darkness Ablaze",
    "swsh35": "Champion's Path",
    "swsh4": "Vivid Voltage",
    "swsh45": "Shining Fates",
    "swsh5": "Battle Styles",
    "swsh6": "Chilling Reign",
    "swsh7": "Evolving Skies",
    "swsh8": "Fusion Strike",
    "swsh9": "Brilliant Stars",
    "swsh10": "Astral Radiance",
    "swsh11": "Lost Origin",
    "swsh12": "Silver Tempest",
    "swsh12pt5": "Crown Zenith",
    "tk1a": "EX Trainer Kit Latias",
    "tk1b": "EX Trainer Kit Latios",
    "tk2a": "EX Trainer Kit 2 Plusle",
    "tk2b": "EX Trainer Kit 2 Minun",
    "xy0": "Kalos Starter Set",
    "xy1": "XY",
    "xy2": "Flashfire",
    "xy3": "Furious Fists",
    "xy4": "Phantom Forces",
    "xy5": "Primal Clash",
    "xy6": "Roaring Skies",
    "xy7": "Ancient Origins",
    "xy8": "BREAKthrough",
    "xy9": "BREAKpoint",
    "xy10": "Fates Collide",
    "xy11": "Steam Siege",
    "xy12": "Evolutions",
    "zsv10pt5": "Scarlet & Violet—Black Bolt",
}


def _load_cards_from_file(json_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        if isinstance(payload.get("cards"), list):
            return [item for item in payload["cards"] if isinstance(item, dict)]

        # Some repos may store one card per file.
        if payload.get("id") and payload.get("name"):
            return [payload]

    raise ValueError(
        f"Unsupported JSON structure in {json_path}. "
        "Expected a list of cards, a {'cards': [...]} object, or a single card object."
    )


def _read_variants(card: dict[str, Any]) -> dict[str, bool]:
    variants = card.get("variants")
    if isinstance(variants, dict):
        return {
            "normal": bool(variants.get("normal", False)),
            "reverse": bool(variants.get("reverse", False)),
            "holo": bool(variants.get("holo", False)),
            "first_edition": bool(variants.get("firstEdition", False)),
            "w_promo": bool(variants.get("wPromo", False)),
        }

    # TODO: This source sample does not include explicit variant availability.
    # For now, assume a standard normal printing is available so collection flows
    # remain usable. Revisit this if the chosen repo exposes richer variant data.
    return {
        "normal": True,
        "reverse": False,
        "holo": False,
        "first_edition": False,
        "w_promo": False,
    }


def _pick_image_url(card: dict[str, Any]) -> str | None:
    images = card.get("images")
    if isinstance(images, dict):
        large = images.get("large")
        if large:
            return str(large)

        small = images.get("small")
        if small:
            return str(small)

    image_url = card.get("image")
    if image_url:
        return str(image_url)

    return None


def _normalize_suffix_variants(suffix: str) -> set[str]:
    if not suffix:
        return {""}

    variants = {suffix}
    if any(char.isalpha() for char in suffix):
        variants.add(suffix.lower())
        variants.add(suffix.upper())
    return variants


def _add_number_aliases(
    aliases: set[str],
    prefix: str,
    local_number: str,
    suffix: str,
) -> None:
    normalized_number = str(int(local_number))
    padded_number = f"{int(local_number):03d}"
    for suffix_variant in _normalize_suffix_variants(suffix):
        aliases.add(f"{prefix}-{normalized_number}{suffix_variant}")
        aliases.add(f"{prefix}-{padded_number}{suffix_variant}")


def _add_dotted_half_set_aliases(
    aliases: set[str],
    card_id: str,
) -> None:
    dotted_prefix_aliases = {
        "sm35": "sm3.5",
        "sm75": "sm7.5",
        "swsh35": "swsh3.5",
        "swsh45": "swsh4.5",
        "swsh12pt5": "swsh12.5",
        "sv3pt5": "sv3.5",
        "sv4pt5": "sv4.5",
        "sv6pt5": "sv6.5",
        "sv8pt5": "sv8.5",
        "me2pt5": "me2.5",
        "zsv10pt5": "zsv10.5",
        "rsv10pt5": "rsv10.5",
    }

    dotted_half_set_match = re.match(
        r"^("
        r"sm35|sm75|swsh35|swsh45|swsh12pt5|"
        r"sv3pt5|sv4pt5|sv6pt5|sv8pt5|"
        r"me2pt5|zsv10pt5|rsv10pt5"
        r")-0*(\d+)([A-Za-z0-9]*)$",
        card_id,
        re.IGNORECASE,
    )
    if not dotted_half_set_match:
        return

    raw_prefix, local_number, suffix = dotted_half_set_match.groups()
    source_prefix = raw_prefix.lower()
    dotted_prefix = dotted_prefix_aliases[source_prefix]

    _add_number_aliases(aliases, source_prefix, local_number, suffix)
    _add_number_aliases(aliases, dotted_prefix, local_number, suffix)

    scarlet_violet_half_match = re.match(r"^sv(\d+)pt5$", source_prefix)
    if scarlet_violet_half_match:
        set_number = int(scarlet_violet_half_match.group(1))
        _add_number_aliases(aliases, f"sv{set_number}.5", local_number, suffix)
        _add_number_aliases(aliases, f"sv{set_number:02d}.5", local_number, suffix)


def generate_card_id_aliases(card_id: str) -> set[str]:
    normalized_card_id = card_id.strip()
    aliases = {normalized_card_id}

    generic_numeric_match = re.match(
        r"^([a-z0-9.]+)-0*(\d+)([A-Za-z0-9]*)$",
        normalized_card_id,
        re.IGNORECASE,
    )
    if generic_numeric_match:
        prefix, local_number, suffix = generic_numeric_match.groups()
        _add_number_aliases(aliases, prefix.lower(), local_number, suffix)

    _add_dotted_half_set_aliases(aliases, normalized_card_id)

    scarlet_violet_match = re.match(
        r"^sv0*(\d+)-0*(\d+)([A-Za-z0-9]*)$",
        normalized_card_id,
        re.IGNORECASE,
    )
    if scarlet_violet_match:
        set_number, local_number, suffix = scarlet_violet_match.groups()
        for suffix_variant in _normalize_suffix_variants(suffix):
            aliases.add(f"sv{int(set_number)}-{int(local_number)}{suffix_variant}")
            aliases.add(f"sv{int(set_number)}-{int(local_number):03d}{suffix_variant}")
            aliases.add(f"sv{int(set_number):02d}-{int(local_number)}{suffix_variant}")
            aliases.add(f"sv{int(set_number):02d}-{int(local_number):03d}{suffix_variant}")

    sword_shield_match = re.match(
        r"^swsh(\d+(?:\.\d+)?)-0*(\d+)([A-Za-z0-9]*)$",
        normalized_card_id,
        re.IGNORECASE,
    )
    if sword_shield_match:
        set_number, local_number, suffix = sword_shield_match.groups()
        for suffix_variant in _normalize_suffix_variants(suffix):
            aliases.add(f"swsh{set_number}-{int(local_number)}{suffix_variant}")
            aliases.add(f"swsh{set_number}-{int(local_number):03d}{suffix_variant}")

    celebrations_match = re.match(r"^cel25c-(\d+)_A(\d*)$", normalized_card_id, re.IGNORECASE)
    if celebrations_match:
        number, suffix = celebrations_match.groups()
        aliases.add(f"cel25-{number}A{suffix}")

    holo_match = re.match(r"^(ecard[23]-H)(\d+)$", normalized_card_id, re.IGNORECASE)
    if holo_match:
        prefix, number = holo_match.groups()
        aliases.add(f"{prefix}{int(number):02d}")

    ecard_variant_match = re.match(r"^(ecard[23]-\d+)$", normalized_card_id, re.IGNORECASE)
    if ecard_variant_match:
        base_id = ecard_variant_match.group(1)
        aliases.add(f"{base_id}a")
        aliases.add(f"{base_id}b")

    return aliases


def card_id_priority(card_id: str) -> tuple[int, int, int, str]:
    prefix, _, local_part = card_id.partition("-")
    local_match = re.match(r"^0*(\d+)([A-Za-z0-9]*)$", local_part)
    local_number = int(local_match.group(1)) if local_match else 0
    suffix = local_match.group(2) if local_match else ""

    prefix_score = 0
    if "pt5" in prefix:
        prefix_score += 20
    if re.match(r"^sv\d+\.\d+$", prefix):
        prefix_score -= 5
    if re.match(r"^sv\d{2}(?:\.\d+)?$", prefix):
        prefix_score -= 5
    if re.match(r"^swsh\d+\.\d+$", prefix):
        prefix_score -= 3

    local_score = 0
    numeric_match = re.match(r"^(0*\d+)", local_part)
    if numeric_match:
        raw_numeric = numeric_match.group(1)
        if len(raw_numeric) < 3:
            local_score += 10
        elif len(raw_numeric) == 3:
            local_score -= 2

    suffix_score = 0
    if suffix and suffix != suffix.upper():
        suffix_score += 5

    return (prefix_score, local_score, suffix_score, card_id)


def resolve_target_card_id(
    source_card_id: str,
    existing_cards_by_id: dict[str, dict[str, Any]],
) -> str:
    matches = [
        alias
        for alias in generate_card_id_aliases(source_card_id)
        if alias in existing_cards_by_id
    ]
    if matches:
        return min(matches, key=card_id_priority)

    return source_card_id


def _build_existing_card_index() -> dict[str, dict[str, Any]]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select
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
                from public.cards
                """
            )
            return {row["id"]: row for row in cursor.fetchall()}


def _derive_set_context(
    card: dict[str, Any],
    json_path: Path,
    cli_set_id: str | None,
    cli_set_name: str | None,
    existing_card: dict[str, Any] | None,
) -> tuple[str, str]:
    if existing_card and existing_card.get("set_id") and existing_card.get("set_name"):
        return str(existing_card["set_id"]), str(existing_card["set_name"])

    if cli_set_id and cli_set_name:
        return cli_set_id, cli_set_name

    set_info = card.get("set")
    if isinstance(set_info, dict):
        set_id = set_info.get("id")
        set_name = set_info.get("name")
        if set_id and set_name:
            return str(set_id), str(set_name)

    inferred_set_id = cli_set_id or card.get("set_id") or card.get("setCode")
    inferred_set_name = cli_set_name or card.get("set_name") or card.get("setName")
    if inferred_set_id and inferred_set_name:
        return str(inferred_set_id), str(inferred_set_name)

    # Fallback for repos that store one JSON file per set, such as `pop1.json`.
    if json_path.stem:
        inferred_name = cli_set_name or LOCAL_SET_NAME_OVERRIDES.get(json_path.stem)
        if inferred_name:
            return json_path.stem, inferred_name

        return json_path.stem, json_path.stem

    raise ValueError(
        f"Could not determine set_id/set_name for card '{card.get('id')}' in {json_path}. "
        "Pass --set-id and --set-name, or use a source file that includes set metadata."
    )


def upsert_card(
    cursor,
    card: dict[str, Any],
    target_card_id: str,
    json_path: Path,
    cli_set_id: str | None,
    cli_set_name: str | None,
    existing_card: dict[str, Any] | None,
) -> None:
    set_id, set_name = _derive_set_context(
        card,
        json_path,
        cli_set_id,
        cli_set_name,
        existing_card,
    )
    source_variants = _read_variants(card)
    existing_variants = existing_card or {}
    variants = {
        "normal": source_variants["normal"] if "variants" in card else bool(existing_variants.get("variant_normal", True)),
        "reverse": source_variants["reverse"] if "variants" in card else bool(existing_variants.get("variant_reverse", False)),
        "holo": source_variants["holo"] if "variants" in card else bool(existing_variants.get("variant_holo", False)),
        "first_edition": source_variants["first_edition"] if "variants" in card else bool(existing_variants.get("variant_first_edition", False)),
        "w_promo": source_variants["w_promo"] if "variants" in card else bool(existing_variants.get("variant_w_promo", False)),
    }
    image_url = _pick_image_url(card) or (existing_card.get("image_url") if existing_card else None)
    local_id = str(card.get("number") or card.get("localId") or "") or None
    category = str(card.get("supertype") or card.get("category") or "") or None
    illustrator = str(card.get("artist") or card.get("illustrator") or "") or None
    rarity = str(card.get("rarity") or "") or None

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
            target_card_id,
            local_id or (existing_card.get("local_id") if existing_card else None),
            str(card["name"]) or (existing_card.get("name") if existing_card else None),
            image_url,
            category or (existing_card.get("category") if existing_card else None),
            illustrator or (existing_card.get("illustrator") if existing_card else None),
            rarity or (existing_card.get("rarity") if existing_card else None),
            set_id,
            set_name,
            variants["normal"],
            variants["reverse"],
            variants["holo"],
            variants["first_edition"],
            variants["w_promo"],
            card.get("updatedAt") or card.get("updated") or (existing_card.get("updated_at_source") if existing_card else None),
        ),
    )


def import_json_file(
    json_path: Path,
    existing_cards_by_id: dict[str, dict[str, Any]],
    cli_set_id: str | None = None,
    cli_set_name: str | None = None,
) -> ImportStats:
    cards = _load_cards_from_file(json_path)
    stats = ImportStats(source_path=str(json_path))

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            for card in cards:
                if not card.get("id") or not card.get("name"):
                    continue
                stats.cards_seen += 1
                source_card_id = str(card["id"])
                target_card_id = resolve_target_card_id(source_card_id, existing_cards_by_id)
                existing_card = existing_cards_by_id.get(target_card_id)
                upsert_card(
                    cursor,
                    card,
                    target_card_id,
                    json_path,
                    cli_set_id,
                    cli_set_name,
                    existing_card,
                )
                stats.cards_upserted += 1

        connection.commit()

    return stats


def _iter_json_files(source: Path) -> list[Path]:
    if source.is_file():
        return [source]

    return sorted(path for path in source.rglob("*.json") if path.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a local card JSON repo into public.cards.",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to a JSON file or directory of JSON files from the external repo.",
    )
    parser.add_argument(
        "--set-id",
        help="Optional set_id override when a source file lacks set metadata.",
    )
    parser.add_argument(
        "--set-name",
        help="Optional set_name override when a source file lacks set metadata.",
    )
    parser.add_argument(
        "--include-supplemental",
        action="store_true",
        help=(
            "Include promo/alternate/subset JSON files that are skipped by default "
            "to reduce duplicate-looking cards in the app."
        ),
    )
    args = parser.parse_args()

    source_path = Path(args.source).expanduser().resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Source path does not exist: {source_path}")

    json_files = _iter_json_files(source_path)
    existing_cards_by_id = _build_existing_card_index()
    total_seen = 0
    total_upserted = 0

    for json_file in json_files:
        if not args.include_supplemental and json_file.stem in SUPPLEMENTAL_SET_IDS:
            print(f"- {json_file.name}: skipped supplemental set", flush=True)
            continue

        stats = import_json_file(
            json_file,
            existing_cards_by_id=existing_cards_by_id,
            cli_set_id=args.set_id,
            cli_set_name=args.set_name,
        )
        total_seen += stats.cards_seen
        total_upserted += stats.cards_upserted
        print(
            f"- {json_file.name}: {stats.cards_upserted}/{stats.cards_seen} cards upserted",
            flush=True,
        )

    print(
        f"Done. Local JSON import total: {total_upserted}/{total_seen} cards upserted.",
        flush=True,
    )


if __name__ == "__main__":
    main()
