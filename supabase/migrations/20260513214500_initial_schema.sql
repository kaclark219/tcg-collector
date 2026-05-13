begin;

create extension if not exists pgcrypto;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table public.profiles (
  id uuid primary key default gen_random_uuid(),
  username text not null,
  pin_hash text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint profiles_username_not_blank check (char_length(trim(username)) > 0)
);

create unique index profiles_username_key
  on public.profiles (username);

create table public.cards (
  id text primary key,
  local_id text,
  name text not null,
  image_url text,
  category text,
  illustrator text,
  rarity text,
  set_id text,
  set_name text,
  variant_normal boolean not null default false,
  variant_reverse boolean not null default false,
  variant_holo boolean not null default false,
  variant_first_edition boolean not null default false,
  variant_w_promo boolean not null default false,
  updated_at_source timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.binders (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles(id) on delete cascade,
  name text not null,
  description text,
  is_system boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint binders_name_not_blank check (char_length(trim(name)) > 0)
);

create unique index binders_profile_id_name_key
  on public.binders (profile_id, name);

create index binders_profile_id_idx
  on public.binders (profile_id);

create unique index binders_one_system_per_profile_idx
  on public.binders (profile_id)
  where is_system = true;

create unique index binders_id_profile_id_key
  on public.binders (id, profile_id);

create table public.collection_entries (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles(id) on delete cascade,
  card_id text not null references public.cards(id) on delete restrict,
  binder_id uuid not null,
  variant text not null default 'unknown',
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint collection_entries_variant_not_blank check (char_length(trim(variant)) > 0),
  constraint collection_entries_binder_profile_fkey
    foreign key (binder_id, profile_id)
    references public.binders (id, profile_id)
    on delete restrict
);

create index collection_entries_profile_id_idx
  on public.collection_entries (profile_id);

create index collection_entries_card_id_idx
  on public.collection_entries (card_id);

create index collection_entries_binder_id_idx
  on public.collection_entries (binder_id);

create index collection_entries_profile_id_binder_id_idx
  on public.collection_entries (profile_id, binder_id);

create index collection_entries_profile_id_card_id_idx
  on public.collection_entries (profile_id, card_id);

create table public.scan_sessions (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references public.profiles(id) on delete cascade,
  status text not null default 'pending',
  candidates_json jsonb,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null,
  constraint scan_sessions_status_check
    check (status in ('pending', 'completed', 'confirmed')),
  constraint scan_sessions_expires_after_created_check
    check (expires_at > created_at)
);

create index scan_sessions_profile_id_idx
  on public.scan_sessions (profile_id);

create index scan_sessions_status_idx
  on public.scan_sessions (status);

create index scan_sessions_expires_at_idx
  on public.scan_sessions (expires_at);

create trigger set_profiles_updated_at
before update on public.profiles
for each row
execute function public.set_updated_at();

create trigger set_cards_updated_at
before update on public.cards
for each row
execute function public.set_updated_at();

create trigger set_binders_updated_at
before update on public.binders
for each row
execute function public.set_updated_at();

create trigger set_collection_entries_updated_at
before update on public.collection_entries
for each row
execute function public.set_updated_at();

commit;

