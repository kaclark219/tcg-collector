# Pokemon Card Collector

Monorepo scaffold for a Pokemon card collection tracker with:

- `apps/mobile`: Expo React Native frontend
- `services/api`: FastAPI backend with mock responses
- `docs`: architecture, schema planning prompts, and roadmap
- `supabase`: SQL migrations and local database tooling

This repo intentionally avoids a finalized production schema for now. The current goal is to establish a clean structure, mock flows, and clear TODOs so the product can evolve without painting you into a corner.

## Project Structure

```text
pokemon-card-collector/
  apps/
    mobile/
  services/
    api/
  docs/
  README.md
```

## Frontend Setup

```bash
cd apps/mobile
npm install
npm run start
```

Useful commands:

```bash
npm run android
npm run ios
npm run web
```

The mobile app expects the API at `http://localhost:8000` by default. For a physical device, update the API base URL in `apps/mobile/src/services/apiClient.ts` or move it to Expo environment config later.
The current scaffold points to `http://127.0.0.1:8003` in `apps/mobile/src/services/apiClient.ts` to match the current local backend setup.

## Backend Setup

```bash
cd services/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will start at `http://127.0.0.1:8000`.

## Database Setup

The first SQL schema now lives in `supabase/migrations/`.

If you are new to Supabase, follow [docs/supabase-setup.md](/home/mygblvsh/Documents/Programming/tcg-collector/docs/supabase-setup.md).

Short version:

```bash
npx supabase init
npx supabase start
npx supabase db reset
```

## TCGdex Import

To load real cards into `public.cards`, use the backend importer documented in [docs/tcgdex-import.md](/home/mygblvsh/Documents/Programming/tcg-collector/docs/tcgdex-import.md).

Darkness Ablaze example:

```bash
cd services/api
source .venv/bin/activate
python -m app.scripts.import_tcgdex_set --set-id swsh3
```

## Current Milestone

- Expo app scaffold with navigation and placeholder screens
- FastAPI scaffold with router groups and mock responses
- Frontend API layer and reusable components
- Architecture, schema-planning, and roadmap docs
- Initial SQL schema and Supabase migration scaffold

## Suggested Next Step

Connect the FastAPI service to the real database schema one slice at a time:

1. Add a database connection layer.
2. Implement `profiles` login with `username` + hashed PIN.
3. Create binder CRUD plus fallback `Unassigned` binder creation.
4. Replace mock collection endpoints with real `collection_entries` queries.
