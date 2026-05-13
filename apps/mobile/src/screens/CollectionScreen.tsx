import { useEffect, useState } from "react";
import { CollectionEntryCard } from "@/components/CollectionEntryCard";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";
import { getCardById } from "@/services/cardsApi";
import { deleteCollectionEntry, getCollectionEntries } from "@/services/collectionApi";
import { Card, CollectionEntry } from "@/types";

export function CollectionScreen() {
  const { profile } = useAuth();
  const [entries, setEntries] = useState<CollectionEntry[]>([]);
  const [cardsById, setCardsById] = useState<Record<string, Card>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCollection() {
      if (!profile) {
        setEntries([]);
        setCardsById({});
        setLoading(false);
        return;
      }

      setLoading(true);
      const collectionEntries = await getCollectionEntries(profile.id);
      setEntries(collectionEntries);

      const uniqueCardIds = [...new Set(collectionEntries.map((entry) => entry.cardId))];
      const loadedCards = await Promise.all(uniqueCardIds.map((cardId) => getCardById(cardId)));

      const nextCardsById: Record<string, Card> = {};
      loadedCards.forEach((card) => {
        if (card) {
          nextCardsById[card.id] = card;
        }
      });
      setCardsById(nextCardsById);
      setLoading(false);
    }

    void loadCollection();
  }, [profile]);

  async function handleDelete(entryId: string) {
    await deleteCollectionEntry(entryId);
    setEntries((current) => current.filter((entry) => entry.id !== entryId));
  }

  return (
    <ScreenLayout
      title="Collection"
      subtitle="Collection entries represent user-owned copies, not master card records."
    >
      {loading ? <LoadingState label="Loading collection..." /> : null}
      {!loading && entries.length === 0 ? (
        <EmptyState
          title="No collection entries yet"
          message="Add a card from search or card detail to start your collection."
        />
      ) : null}
      {entries.map((entry) => (
        <CollectionEntryCard
          key={entry.id}
          entry={entry}
          card={cardsById[entry.cardId]}
          onDelete={() => {
            void handleDelete(entry.id);
          }}
        />
      ))}
    </ScreenLayout>
  );
}
