begin;

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
  'swsh3-136',
  '136',
  'Furret',
  'https://assets.tcgdex.net/en/swsh/swsh3/136',
  'Pokemon',
  'tetsuya koizumi',
  'Uncommon',
  'swsh3',
  'Darkness Ablaze',
  true,
  true,
  false,
  false,
  false,
  '2024-02-04T22:55:32+02:00'::timestamptz
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
  updated_at_source = excluded.updated_at_source;

commit;

