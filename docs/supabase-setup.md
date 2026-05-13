# Supabase Setup

This project now includes SQL migrations under `supabase/migrations/`.

If you have never used Supabase before, this is the simplest path:

## What Supabase Is Doing Here

For this project, Supabase is mainly being used as:

- hosted Postgres later
- local Postgres for development now
- migration tooling through the Supabase CLI

The current schema does **not** depend on Supabase Auth. We are using a local `profiles` table instead.

## Prerequisites

You need:

- Docker or a compatible container runtime
- Node.js installed

Supabase recommends using the CLI for local development.

## First-Time Local Setup

From the repo root:

```bash
npx supabase init
```

This creates `supabase/config.toml`, which the CLI needs for local development.

Then start the local Supabase stack:

```bash
npx supabase start
```

Then apply the migrations in this repo:

```bash
npx supabase db reset
```

That command applies everything in `supabase/migrations/` and also runs `supabase/seed.sql`.

## Backend Database Connection

The FastAPI service reads its database URL from one of these environment variables:

- `DATABASE_URL`
- `SUPABASE_DB_URL`

The backend now also loads:

- repo root `.env`
- `services/api/.env`

The service-specific file wins if both exist.

Example:

```bash
export DATABASE_URL="postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres"
```

If you prefer the Supabase pooler, that can work too as long as the connection string is valid for normal Postgres access.

Recommended setup:

1. Copy [services/api/.env.example](/home/mygblvsh/Documents/Programming/tcg-collector/services/api/.env.example) to `services/api/.env`
2. Paste your real `DATABASE_URL`
3. Start the API normally

Example:

```bash
cd services/api
cp .env.example .env
```

## Useful Commands

Start local services:

```bash
npx supabase start
```

Stop local services:

```bash
npx supabase stop
```

Re-apply all migrations from scratch:

```bash
npx supabase db reset
```

Create a new migration file later:

```bash
npx supabase migration new describe_change
```

## When You Create A Real Hosted Supabase Project

Later, after creating a project in the Supabase dashboard:

```bash
npx supabase login
npx supabase link --project-ref <your-project-ref>
npx supabase db push
```

Use `db push` only after reviewing your local migrations carefully.

## Notes For This Project

- `cards` is global/shared catalog data
- `profiles`, `binders`, `collection_entries`, and `scan_sessions` are profile-owned
- `scan_candidates` is not a separate table in this version
- fallback binder creation is still expected to happen in app/service logic, not purely in SQL

## Current Test Profile

The repo currently includes a seeded development profile:

- username: `mygblvsh`
- PIN: `021903`

This is only appropriate for your current personal project setup and should be changed before treating the app as a real multi-user deployment.
