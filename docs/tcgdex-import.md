# TCGdex Import

This project now includes a backend import script for loading cards from TCGdex into `public.cards`.

## Recommended SDK

Use the Python SDK in the FastAPI/backend project:

- package: `tcgdex-sdk`
- docs: https://tcgdex.dev/sdks/python
- SDK overview: https://tcgdex.dev/sdks

## Important Set ID Note

For Darkness Ablaze, use:

- `swsh3`

Not:

- `swsh-3`

TCGdex card IDs and set IDs use the compact form like `swsh3-136` and `swsh3`.

Common Sword & Shield era TCGdex IDs:

- `swsh1` = Sword & Shield
- `swsh2` = Rebel Clash
- `swsh3` = Darkness Ablaze
- `swsh3.5` = Champion's Path
- `swsh4` = Vivid Voltage
- `swsh4.5` = Shining Fates
- `swsh5` = Battle Styles
- `swsh6` = Chilling Reign
- `swsh7` = Evolving Skies
- `cel25` = Celebrations
- `swsh8` = Fusion Strike
- `swsh9` = Brilliant Stars
- `swsh10` = Astral Radiance
- `swsh10.5` = Pokémon GO
- `swsh11` = Lost Origin
- `swsh12` = Silver Tempest
- `swsh12.5` = Crown Zenith

## What The Importer Does

The script:

1. fetches the set from TCGdex
2. loops through the set’s card list
3. fetches each full card record
4. upserts each card into `public.cards`

It maps only the columns your schema currently stores:

- `id`
- `local_id`
- `name`
- `image_url`
- `category`
- `illustrator`
- `rarity`
- `set_id`
- `set_name`
- variant booleans
- `updated_at_source`

## Step By Step

### 1. Install the SDK in the backend environment

```bash
cd /home/mygblvsh/Documents/Programming/tcg-collector/services/api
source .venv/bin/activate
pip install -r requirements.txt
```

That now includes:

- `tcgdex-sdk==2.3.0`

### 2. Make sure your database connection is still configured

Your `services/api/.env` should already contain:

```env
DATABASE_URL=postgresql://...
```

### 3. Run the Darkness Ablaze import

From `services/api`:

```bash
source .venv/bin/activate
python -m app.scripts.import_tcgdex_set --set-id swsh3
```

### 4. Verify the cards were imported

You can test through the API:

```bash
curl "http://127.0.0.1:8003/cards/search?q=furret"
```

Or in Supabase SQL editor:

```sql
select id, name, local_id, set_name
from public.cards
where set_id = 'swsh3'
order by local_id;
```

## Expected Result

The script should print something like:

```text
Imported set Darkness Ablaze (swsh3): 201/201 cards upserted.
```

The exact number depends on what TCGdex currently returns for that set.

## Import The Full Sword & Shield Series

This project also includes a convenience script for the whole Sword & Shield block:

```bash
cd /home/mygblvsh/Documents/Programming/tcg-collector/services/api
source .venv/bin/activate
python -m app.scripts.import_tcgdex_sword_shield
```

This imports:

- Sword & Shield
- Rebel Clash
- Darkness Ablaze
- Champion's Path
- Vivid Voltage
- Shining Fates
- Battle Styles
- Chilling Reign
- Evolving Skies
- Celebrations
- Fusion Strike
- Brilliant Stars
- Astral Radiance
- Pokémon GO
- Lost Origin
- Silver Tempest
- Crown Zenith

## Notes

- The importer is safe to re-run because it uses `upsert` behavior.
- This script currently imports one set at a time.
- It does not yet import advanced metadata like attacks, weaknesses, or pricing because your schema intentionally does not store those yet.
