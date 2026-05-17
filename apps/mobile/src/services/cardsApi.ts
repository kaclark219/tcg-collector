import { mockCards } from "@/data/mockData";
import { API_BASE_URL, apiRequest } from "@/services/apiClient";
import { normalizeTcgdexImageUrl } from "@/services/tcgdexImages";
import { Card } from "@/types";

type ApiCard = {
  id: string;
  name: string;
  set_name?: string;
  number: string;
  rarity: string;
  image_url?: string;
  variant_normal?: boolean;
  variant_reverse?: boolean;
  variant_holo?: boolean;
  variant_first_edition?: boolean;
  variant_w_promo?: boolean;
};

function normalizeCard(card: ApiCard): Card {
  const directImageUrl = normalizeTcgdexImageUrl(card.image_url);

  return {
    id: card.id,
    name: card.name,
    setName: card.set_name ?? "Unknown set",
    number: card.number,
    rarity: card.rarity,
    imageUrl: directImageUrl ? `${API_BASE_URL}/cards/${card.id}/image` : undefined,
    variantNormal: card.variant_normal ?? false,
    variantReverse: card.variant_reverse ?? false,
    variantHolo: card.variant_holo ?? false,
    variantFirstEdition: card.variant_first_edition ?? false,
    variantWPromo: card.variant_w_promo ?? false,
  };
}

export async function searchCards(query: string): Promise<Card[]> {
  try {
    const result = await apiRequest<{ cards: ApiCard[] }>(
      `/cards/search?q=${encodeURIComponent(query)}`,
    );

    return result.cards.map(normalizeCard);
  } catch {
    const normalized = query.trim().toLowerCase();
    return mockCards.filter((card) =>
      `${card.name} ${card.setName} ${card.number}`
        .toLowerCase()
        .includes(normalized),
    );
  }
}

export async function getCardById(cardId: string): Promise<Card | undefined> {
  try {
    const card = await apiRequest<ApiCard>(`/cards/${cardId}`);
    return normalizeCard(card);
  } catch {
    return mockCards.find((card) => card.id === cardId);
  }
}
