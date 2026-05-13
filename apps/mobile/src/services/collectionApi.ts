import { mockCollectionEntries } from "@/data/mockData";
import { apiRequest } from "@/services/apiClient";
import { CollectionEntry } from "@/types";

type ApiCollectionEntry = {
  id: string;
  profile_id: string;
  card_id: string;
  binder_id: string;
  variant: string;
  notes?: string | null;
};

function normalizeCollectionEntry(entry: ApiCollectionEntry): CollectionEntry {
  return {
    id: entry.id,
    profileId: entry.profile_id,
    cardId: entry.card_id,
    binderId: entry.binder_id,
    variant: entry.variant,
    notes: entry.notes ?? undefined,
  };
}

export async function getCollectionEntries(
  profileId: string,
  binderId?: string,
): Promise<CollectionEntry[]> {
  try {
    const search = new URLSearchParams({ profile_id: profileId });
    if (binderId) {
      search.set("binder_id", binderId);
    }
    const entries = await apiRequest<ApiCollectionEntry[]>(`/collection?${search.toString()}`);
    return entries.map(normalizeCollectionEntry);
  } catch {
    return mockCollectionEntries.filter(
      (entry) =>
        entry.profileId === "mock-profile" && (!binderId || entry.binderId === binderId),
    );
  }
}

export async function getCollectionEntryById(
  entryId: string,
): Promise<CollectionEntry | undefined> {
  try {
    const entry = await apiRequest<ApiCollectionEntry>(`/collection/${entryId}`);
    return normalizeCollectionEntry(entry);
  } catch {
    return mockCollectionEntries.find((entry) => entry.id === entryId);
  }
}

export async function createCollectionEntry(input: {
  profileId: string;
  cardId: string;
  binderId: string;
  variant: string;
  notes?: string;
}): Promise<CollectionEntry> {
  const entry = await apiRequest<ApiCollectionEntry>("/collection", {
    method: "POST",
    body: {
      profile_id: input.profileId,
      card_id: input.cardId,
      binder_id: input.binderId,
      variant: input.variant,
      notes: input.notes,
    },
  });

  return normalizeCollectionEntry(entry);
}

export async function moveCollectionEntry(
  entryId: string,
  binderId: string,
): Promise<{ success: boolean }> {
  try {
    return await apiRequest<{ success: boolean }>("/collection/move", {
      method: "POST",
      body: { entry_id: entryId, binder_id: binderId },
    });
  } catch {
    return { success: true };
  }
}

export async function deleteCollectionEntry(
  entryId: string,
): Promise<{ success: boolean }> {
  return apiRequest<{ success: boolean }>(`/collection/${entryId}`, {
    method: "DELETE",
  });
}
