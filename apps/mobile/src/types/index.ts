export type Card = {
  id: string;
  name: string;
  setName: string;
  number: string;
  rarity: string;
  imageUrl?: string;
  variantNormal?: boolean;
  variantReverse?: boolean;
  variantHolo?: boolean;
  variantFirstEdition?: boolean;
  variantWPromo?: boolean;
};

export type Binder = {
  id: string;
  name: string;
  description?: string;
  entryCount: number;
};

export type Profile = {
  id: string;
  username: string;
};

export type CollectionEntry = {
  id: string;
  profileId: string;
  cardId: string;
  binderId: string;
  variant: string;
  notes?: string;
};

export type ScanCandidate = {
  id: string;
  cardId: string;
  confidence: number;
  reason: string;
};

export type ScanSession = {
  id: string;
  status: "pending" | "completed" | "confirmed";
  imageUrl?: string;
  candidates: ScanCandidate[];
};

export type SearchResponse = {
  cards: Card[];
};

export type LoginResponse = {
  profile: Profile;
};
