# Schema Planning

This document captures the current agreed schema direction before writing SQL migrations.

It is intentionally:

- concise
- reviewable
- implementation-oriented
- not yet a migration file

Current simplified table set:

- `profiles`
- `cards`
- `binders`
- `collection_entries`
- `scan_sessions`

There is no separate `scan_candidates` table in this version. Candidate matches are embedded in `scan_sessions.candidates_json`.

## Table Summary

### `profiles`

Local account records used for lightweight app login. This app is intended for simple personal use, so profiles are kept minimal and separate from the shared card catalog.

### `cards`

Master catalog card records sourced from TCGdex. This table is lean and collection-focused, not a full mirror of all upstream metadata.

### `binders`

Lightweight profile-owned category/group records. Binders organize `collection_entries`, not master cards.

### `collection_entries`

One row per physical owned card. Each row belongs to a profile, one binder, and one master card.

### `scan_sessions`

Temporary scan workflow records. These hold short-lived candidate match data until the user confirms one and a `collection_entries` row is created.

## `profiles`

### Summary

- `profiles` stores lightweight local account records for the app
- usernames should be unique
- login uses `username` plus a six-digit PIN
- store a PIN hash, not the raw PIN
- `username` is enough for now; no separate display name is needed
- `cards` remains global/shared and is not tied to a profile

### Likely Columns

- `id uuid primary key`
- `username text not null`
- `pin_hash text not null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Relationships

- One profile has many `binders`
- One profile has many `collection_entries`
- One profile has many `scan_sessions`

### Constraints And Indexes

- Primary key on `id`
- `unique(username)`

### Service-Layer Behavior

- Validate that login PIN input is exactly six digits before hashing/checking
- Hash and compare PINs in application code
- Do not store the PIN itself in plain text
- Create the fallback system binder for new profiles

## `cards`

### Summary

- Use the TCGdex external card ID as the primary key.
- Keep the table lean and collection-focused.
- Store only common/shared card fields.
- Keep image URL and source update timestamp.
- Do not create a separate `sets` table yet.
- Do not store pricing, attacks, weaknesses, legalities, or long-form card metadata yet.

### Likely Columns

- `id text primary key`
- `local_id text`
- `name text not null`
- `image_url text`
- `category text`
- `illustrator text`
- `rarity text`
- `set_id text`
- `set_name text`
- `variant_normal boolean not null default false`
- `variant_reverse boolean not null default false`
- `variant_holo boolean not null default false`
- `variant_first_edition boolean not null default false`
- `variant_w_promo boolean not null default false`
- `updated_at_source timestamptz`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Notes

- `local_id` should remain `text` because collector numbering can be awkward.
- `category` should remain `text` for now.
- `set_id` and `set_name` live directly on `cards` for now.
- `variant_*` booleans describe what variants exist for the master card, not what the user owns.

### Relationships

- Referenced by `collection_entries.card_id`
- Referenced indirectly by `scan_sessions.candidates_json[*].card_id`

### Constraints And Indexes

- Primary key on `id`
- Additional indexes can be added later once actual search patterns are measured

### Service-Layer Behavior

- Sync/import cards from TCGdex into this table
- Keep source updates mapped into `updated_at_source`
- Do not treat this table as the place for user ownership or user-specific metadata

## `binders`

### Summary

- Binders are lightweight category-style groups.
- Binder names are unique per profile.
- Description is optional.
- Include `is_system`.
- Each profile has one fallback system binder, initially called `Unassigned`.
- System binders can be renamed, so the fallback binder should not be identified by name.
- Deleting a normal binder should reassign entries to the profile’s fallback system binder.
- Sorting is query/UI-driven, so do not add `sort_order` yet.

### Likely Columns

- `id uuid primary key`
- `profile_id uuid not null references profiles(id)`
- `name text not null`
- `description text`
- `is_system boolean not null default false`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Relationships

- One profile has many binders
- One binder has many `collection_entries`
- Referenced by `collection_entries.binder_id`

### Constraints And Indexes

- Primary key on `id`
- `unique(profile_id, name)`
- Index on `profile_id`
- Enforce at most one system binder per profile, likely with a partial unique index on `profile_id where is_system = true`

### Service-Layer Behavior

- Ensure every profile has a fallback system binder
- Prevent deleting a system binder unless another fallback exists or is created first
- Before deleting a normal binder, reassign its collection entries to the profile’s system binder
- Do not identify the fallback binder by literal name

## `collection_entries`

### Summary

- One row per physical owned card
- Each row belongs to a profile
- Each row belongs to a binder
- Each row references one master card
- Use a single `variant` column
- Do not add condition tracking yet
- Duplicates are stored as separate rows
- Grouping/counting happens in queries/UI, not in the base table
- Multiple identical copies in the same binder are allowed
- Moving one card between binders means updating one row
- Moving multiple cards means updating multiple rows

### Likely Columns

- `id uuid primary key`
- `profile_id uuid not null references profiles(id)`
- `card_id text not null references cards(id)`
- `binder_id uuid not null references binders(id)`
- `variant text not null default 'unknown'`
- `notes text`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Relationships

- Many `collection_entries` belong to one profile
- Many `collection_entries` belong to one binder
- Many `collection_entries` reference one master `card`

### Constraints And Indexes

- Primary key on `id`
- No uniqueness constraint that prevents duplicates
- Index on `profile_id`
- Index on `card_id`
- Index on `binder_id`
- Composite index on `(profile_id, binder_id)`
- Composite index on `(profile_id, card_id)`
- Consider index on `(card_id, binder_id, variant)` if grouping queries need it

### Notes

- `notes` should stay nullable and optional
- `variant` is the owned-copy variant
- `cards.variant_*` fields describe variant availability
- `collection_entries.variant` describes the specific owned copy

### Possible Variant Values For Now

- `normal`
- `reverse`
- `holo`
- `first_edition`
- `w_promo`
- `unknown`

Use `text` for now unless there is a strong reason later to move to a DB enum.

### Service-Layer Behavior

- Collapse/group duplicate cards in UI or query logic, not by storing quantity
- Validate that the chosen variant is sensible for the selected card if desired later
- Reassign rows to the fallback binder when a normal binder is deleted

## `scan_sessions`

### Summary

- Temporary only
- No user image storage
- No OCR text storage
- No detailed error fields
- No long-term scan history
- Confirmation immediately creates a `collection_entries` row in the profile’s fallback system binder
- Keep only short-lived candidate data
- Use `candidates_json` instead of a separate `scan_candidates` table

### Likely Columns

- `id uuid primary key`
- `profile_id uuid not null references profiles(id)`
- `status text not null default 'pending'`
- `candidates_json jsonb`
- `created_at timestamptz not null default now()`
- `expires_at timestamptz not null`

### Candidate JSON Shape

```json
[
  {
    "card_id": "tcgdex-card-id",
    "rank": 1,
    "confidence": 0.92
  }
]
```

### Relationships

- Many `scan_sessions` belong to one profile
- Candidate objects in `candidates_json` point to `cards.id`
- Confirming a candidate creates a new `collection_entries` row

### Possible Status Values

- `pending`
- `completed`
- `confirmed`

Do not add `failed` yet unless it becomes necessary later.

### Constraints And Indexes

- Primary key on `id`
- Index on `profile_id`
- Index on `status`
- Index on `expires_at`

### UI Behavior

- Scan result UI reads `candidates_json`
- For each candidate, fetch/join card data from `cards` using `card_id`
- Card image comes from `cards.image_url`
- User picks a candidate
- App creates a `collection_entries` row in the profile’s system fallback binder
- Scan session remains until `expires_at` cleanup

### Service-Layer Behavior

- Expire/delete old scan sessions using `expires_at`
- On confirmation, create a collection entry in the profile’s system binder
- Mark the scan session `confirmed`
- Do not rely on scan sessions as long-term history

## Relationship Notes

- `profiles` stores lightweight local app accounts
- `cards` is the master catalog table
- `binders` are profile-owned organizational groups
- `collection_entries` connects a profile-owned physical copy to one master card and one binder
- `scan_sessions` temporarily points back to candidate cards through embedded JSON
- Profile ownership and organizational state belong in `binders` and `collection_entries`, not in `cards`

## Constraints And Indexes Overview

### Strong candidates for initial migrations

- `profiles`: primary key on `id`
- `profiles`: unique `username`
- `cards`: primary key on `id`
- `binders`: primary key on `id`
- `binders`: unique `(profile_id, name)`
- `binders`: index `profile_id`
- `binders`: partial unique index for one system binder per profile
- `collection_entries`: primary key on `id`
- `collection_entries`: indexes on `profile_id`, `card_id`, `binder_id`
- `collection_entries`: composite indexes on `(profile_id, binder_id)` and `(profile_id, card_id)`
- `scan_sessions`: primary key on `id`
- `scan_sessions`: indexes on `profile_id`, `status`, `expires_at`

### Deferred until query patterns justify them

- full-text or trigram search indexes on `cards`
- additional grouping index for `collection_entries`
- specialized JSON indexes on `scan_sessions.candidates_json`

## Service-Layer Responsibilities

These behaviors should not be treated as solved by SQL alone yet:

- validating and hashing six-digit PINs
- creating and maintaining each profile’s fallback system binder
- preventing unsafe deletion of system binders
- reassigning entries before binder deletion
- syncing/importing card data from TCGdex
- validating candidate confirmation flow before collection row creation
- expiring and deleting temporary scan sessions
- grouping identical owned cards in UI/query logic instead of in the base schema

## Open Questions / TODOs Before Writing Migrations

- Should the six-digit PIN policy be enforced only in application code, or also with a DB-level constraint on a raw/derived field if needed later?
- Should `updated_at` timestamps be trigger-managed in SQL or application-managed?
- Should `cards.name`, `set_name`, and `local_id` get initial search indexes in v1, or wait until search performance is measured?
- Should `collection_entries.variant` remain free text with app validation, or get a check constraint for the current allowed values?
- How should fallback binder creation be bootstrapped for existing profiles versus new profiles?
- What cleanup cadence should be used for expired `scan_sessions`?
- Should `scan_sessions.candidates_json` be required to be non-null when `status = 'completed'`?
- Should binder deletion and reassignment happen in one transaction at the service layer?
