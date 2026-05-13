import psycopg
from psycopg.errors import UndefinedTable

from app.core.db import DatabaseNotConfiguredError, get_db_connection
from app.data.mock_data import MOCK_CARDS
from app.schemas.cards import Card


def _row_to_card(row: dict) -> Card:
    return Card(
        id=row["id"],
        name=row["name"],
        set_name=row.get("set_name") or "Unknown set",
        number=row.get("local_id") or "?",
        rarity=row.get("rarity") or "Unknown rarity",
        image_url=row.get("image_url"),
        category=row.get("category"),
        illustrator=row.get("illustrator"),
        set_id=row.get("set_id"),
        variant_normal=row.get("variant_normal", False),
        variant_reverse=row.get("variant_reverse", False),
        variant_holo=row.get("variant_holo", False),
        variant_first_edition=row.get("variant_first_edition", False),
        variant_w_promo=row.get("variant_w_promo", False),
    )


def search_cards(query: str) -> list[Card]:
    normalized_query = query.strip().lower()
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                if not normalized_query:
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
                          variant_w_promo
                        from public.cards
                        order by name asc
                        limit 50
                        """
                    )
                else:
                    wildcard_query = f"%{normalized_query}%"
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
                          variant_w_promo
                        from public.cards
                        where
                          lower(name) like %s
                          or lower(set_name) like %s
                          or lower(local_id) like %s
                          or lower(id) like %s
                        order by name asc
                        limit 50
                        """,
                        (
                            wildcard_query,
                            wildcard_query,
                            wildcard_query,
                            wildcard_query,
                        ),
                    )
                rows = cursor.fetchall()
            return [_row_to_card(row) for row in rows]
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
        if not normalized_query:
            return [Card(**card) for card in MOCK_CARDS]

        return [
            Card(**card)
            for card in MOCK_CARDS
            if normalized_query
            in f"{card['name']} {card['set_name']} {card['number']} {card['id']}".lower()
        ]


def get_card(card_id: str) -> Card | None:
    try:
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
                      variant_w_promo
                    from public.cards
                    where id = %s
                    limit 1
                    """,
                    (card_id,),
                )
                row = cursor.fetchone()
            if row is None:
                return None
            return _row_to_card(row)
    except (DatabaseNotConfiguredError, UndefinedTable, psycopg.Error):
        for card in MOCK_CARDS:
            if card["id"] == card_id:
                return Card(**card)
        return None
