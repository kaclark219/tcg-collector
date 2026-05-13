import { Binder, Card, CollectionEntry, ScanSession } from "@/types";

export const mockCards: Card[] = [
  {
    id: "base1-4",
    name: "Charizard",
    setName: "Base Set",
    number: "4/102",
    rarity: "Holo Rare",
  },
  {
    id: "base1-2",
    name: "Blastoise",
    setName: "Base Set",
    number: "2/102",
    rarity: "Holo Rare",
  },
  {
    id: "base1-15",
    name: "Venusaur",
    setName: "Base Set",
    number: "15/102",
    rarity: "Holo Rare",
  },
  {
    id: "sv3-125",
    name: "Pikachu",
    setName: "Obsidian Flames",
    number: "125/197",
    rarity: "Common",
  },
];

export const mockBinders: Binder[] = [
  {
    id: "binder-1",
    name: "Favorites",
    description: "Cards I like displaying first.",
    entryCount: 2,
  },
  {
    id: "binder-2",
    name: "Trade Binder",
    description: "Duplicates and trade candidates.",
    entryCount: 2,
  },
  {
    id: "binder-3",
    name: "Unsorted Ideas",
    description: "Placeholder organizer for testing flows.",
    entryCount: 0,
  },
];

export const mockCollectionEntries: CollectionEntry[] = [
  {
    id: "entry-1",
    profileId: "mock-profile",
    cardId: "base1-4",
    binderId: "binder-1",
    variant: "holo",
  },
  {
    id: "entry-2",
    profileId: "mock-profile",
    cardId: "base1-2",
    binderId: "binder-1",
    variant: "holo",
  },
  {
    id: "entry-3",
    profileId: "mock-profile",
    cardId: "sv3-125",
    binderId: "binder-2",
    variant: "normal",
    notes: "Possible trade extras.",
  },
];

export const mockScanSession: ScanSession = {
  id: "scan-1",
  status: "completed",
  candidates: [
    {
      id: "candidate-1",
      cardId: "base1-4",
      confidence: 0.91,
      reason: "Strong text and artwork overlap",
    },
    {
      id: "candidate-2",
      cardId: "base1-2",
      confidence: 0.42,
      reason: "Partial border and text match",
    },
  ],
};
