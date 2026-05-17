# JSON Card Import

This project now includes a local JSON importer for card repositories whose data
looks more like `pokemontcg.io` than TCGdex.

Script:

- `services/api/app/scripts/import_json_card_repo.py`

## Best Import Strategy

Use this second source as a **normalization input**, not as a second schema.

Recommended workflow:

1. Parse source JSON into the existing `public.cards` schema
2. Prefer `images.large` for `cards.image_url`
3. Upsert by card `id`
4. Use CLI `--set-id` and `--set-name` overrides when the source file does not include set metadata
5. Use this source for:
   - newer sets TCGdex does not expose yet
   - image repair/replacement for older sets
   - one-off imports from per-set JSON files

## Current Field Mapping

Source JSON field -> `public.cards`

- `id` -> `id`
- `number` or `localId` -> `local_id`
- `name` -> `name`
- `images.large` preferred, `images.small` fallback -> `image_url`
- `supertype` or `category` -> `category`
- `artist` or `illustrator` -> `illustrator`
- `rarity` -> `rarity`
- `set.id` / `set.name` if present -> `set_id` / `set_name`
- `updatedAt` or `updated` if present -> `updated_at_source`

## Variant Handling

The sample JSON format does not always include explicit variant availability.

Current importer behavior:

- if a `variants` object exists, map it into:
  - `variant_normal`
  - `variant_reverse`
  - `variant_holo`
  - `variant_first_edition`
  - `variant_w_promo`
- otherwise default to:
  - `variant_normal = true`
  - all others `false`

This is a practical fallback so collection flows keep working, but it should be
reviewed if your chosen repo exposes better print/finish metadata.

## Example Usage

Import one file that already contains set metadata:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_json_card_repo --source /path/to/cards/pop1.json
```

Import one file that does **not** contain set metadata:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_json_card_repo \
  --source /path/to/cards/pop1.json \
  --set-id pop1 \
  --set-name "POP Series 1"
```

Import a whole directory of JSON files:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_json_card_repo --source /path/to/repo/cards
```

## Important TODOs

- Confirm the GitHub repo’s folder layout before bulk-importing
- Confirm whether set metadata is present in each file or needs CLI overrides
- Decide whether this source should:
  - fully own certain sets
  - only patch missing TCGdex sets
  - or only repair `image_url`
- Add a `--images-only` mode later if you want safe image backfills without touching names/rarity/set data
