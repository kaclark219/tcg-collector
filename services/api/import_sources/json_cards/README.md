# JSON Drop Folder

Drop external card JSON files here when you want to import them into `public.cards`.

Suggested uses:

- newer sets that TCGdex does not expose yet
- image repair data for older sets
- one-off set files from another repo

Examples:

- `services/api/import_sources/json_cards/pop1.json`
- `services/api/import_sources/json_cards/sv10/black-bolt.json`
- `services/api/import_sources/json_cards/repo-export/cards.json`

To import one file:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_json_card_repo \
  --source import_sources/json_cards/pop1.json \
  --set-id pop1 \
  --set-name "POP Series 1"
```

To import a whole folder:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_json_card_repo \
  --source import_sources/json_cards
```

Notes:

- If a JSON file does not include set metadata, pass `--set-id` and `--set-name`.
- If the source file already includes set metadata, the importer can use that directly.
- Keep raw downloaded files here so we can inspect and adapt the importer if the repo format changes.
