MOCK_CARDS = [
    {
        "id": "base1-4",
        "name": "Charizard",
        "set_name": "Base Set",
        "number": "4/102",
        "rarity": "Holo Rare",
        "image_url": None,
    },
    {
        "id": "base1-2",
        "name": "Blastoise",
        "set_name": "Base Set",
        "number": "2/102",
        "rarity": "Holo Rare",
        "image_url": None,
    },
    {
        "id": "base1-15",
        "name": "Venusaur",
        "set_name": "Base Set",
        "number": "15/102",
        "rarity": "Holo Rare",
        "image_url": None,
    },
    {
        "id": "sv3-125",
        "name": "Pikachu",
        "set_name": "Obsidian Flames",
        "number": "125/197",
        "rarity": "Common",
        "image_url": None,
    },
]

MOCK_BINDERS = [
    {
        "id": "binder-1",
        "name": "Favorites",
        "description": "Cards I like displaying first.",
        "entry_count": 2,
    },
    {
        "id": "binder-2",
        "name": "Trade Binder",
        "description": "Duplicates and trade candidates.",
        "entry_count": 1,
    },
    {
        "id": "binder-3",
        "name": "Unsorted Ideas",
        "description": "Placeholder organizer for testing flows.",
        "entry_count": 0,
    },
]

MOCK_COLLECTION_ENTRIES = [
    {
        "id": "entry-1",
        "card_id": "base1-4",
        "binder_id": "binder-1",
        "quantity": 1,
        "condition": "Near Mint",
        "finish": "Holo",
        "notes": None,
    },
    {
        "id": "entry-2",
        "card_id": "base1-2",
        "binder_id": "binder-1",
        "quantity": 1,
        "condition": "Lightly Played",
        "finish": "Holo",
        "notes": None,
    },
    {
        "id": "entry-3",
        "card_id": "sv3-125",
        "binder_id": "binder-2",
        "quantity": 3,
        "condition": "Near Mint",
        "finish": "Regular",
        "notes": "Possible trade extras.",
    },
]

MOCK_SCAN_SESSIONS = {
    "scan-1": {
        "id": "scan-1",
        "status": "completed",
        "image_url": None,
        "candidates": [
            {
                "id": "candidate-1",
                "card_id": "base1-4",
                "confidence": 0.91,
                "reason": "Strong text and artwork overlap",
            },
            {
                "id": "candidate-2",
                "card_id": "base1-2",
                "confidence": 0.42,
                "reason": "Partial border and text match",
            },
        ],
    }
}

