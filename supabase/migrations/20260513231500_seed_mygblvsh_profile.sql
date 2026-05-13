begin;

with upserted_profile as (
  insert into public.profiles (username, pin_hash)
  values (
    'mygblvsh',
    'pbkdf2_sha256$390000$XxkLTeSdFNpeWESg+hx28w==$82imnDxuSt5HGlZuhVT3B3j2rYaji1cJ+RK9DiCnqO0='
  )
  on conflict (username) do update
  set pin_hash = excluded.pin_hash
  returning id
)
insert into public.binders (profile_id, name, description, is_system)
select
  upserted_profile.id,
  'Unassigned',
  'Default fallback binder for unassigned cards.',
  true
from upserted_profile
where not exists (
  select 1
  from public.binders b
  where b.profile_id = upserted_profile.id
    and b.is_system = true
);

commit;

