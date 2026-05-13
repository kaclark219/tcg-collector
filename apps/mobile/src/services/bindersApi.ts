import { mockBinders } from "@/data/mockData";
import { apiRequest } from "@/services/apiClient";
import { Binder } from "@/types";

function normalizeBinder(binder: {
  id: string;
  name: string;
  description?: string | null;
  entry_count?: number;
  entryCount?: number;
}): Binder {
  return {
    id: binder.id,
    name: binder.name,
    description: binder.description ?? undefined,
    entryCount: binder.entry_count ?? binder.entryCount ?? 0,
  };
}

export async function getBinders(profileId: string): Promise<Binder[]> {
  try {
    const binders = await apiRequest<
      Array<{
        id: string;
        name: string;
        description?: string | null;
        entry_count?: number;
      }>
    >(`/binders?profile_id=${encodeURIComponent(profileId)}`);

    return binders.map(normalizeBinder);
  } catch {
    return mockBinders;
  }
}

export async function getBinderById(
  binderId: string,
  profileId: string,
): Promise<Binder | undefined> {
  try {
    const binder = await apiRequest<{
      id: string;
      name: string;
      description?: string | null;
      entry_count?: number;
    }>(`/binders/${binderId}?profile_id=${encodeURIComponent(profileId)}`);
    return normalizeBinder(binder);
  } catch {
    return mockBinders.find((binder) => binder.id === binderId);
  }
}

export async function createBinder(
  profileId: string,
  name: string,
  description?: string,
): Promise<Binder> {
  const binder = await apiRequest<{
    id: string;
    name: string;
    description?: string | null;
    entry_count?: number;
  }>("/binders", {
    method: "POST",
    body: {
      profile_id: profileId,
      name,
      description,
    },
  });

  return normalizeBinder(binder);
}

