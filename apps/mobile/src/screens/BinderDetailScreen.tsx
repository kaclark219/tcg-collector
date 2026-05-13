import { useEffect, useState } from "react";
import { CollectionEntryCard } from "@/components/CollectionEntryCard";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";
import { getBinderById } from "@/services/bindersApi";
import { getCardById } from "@/services/cardsApi";
import { deleteCollectionEntry, getCollectionEntries } from "@/services/collectionApi";
import { Binder, Card, CollectionEntry } from "@/types";

type BinderDetailScreenProps = {
  binderId: string;
};

export function BinderDetailScreen({ binderId }: BinderDetailScreenProps) {
  const { profile } = useAuth();
  const [binder, setBinder] = useState<Binder | undefined>();
  const [entries, setEntries] = useState<CollectionEntry[]>([]);
  const [cardsById, setCardsById] = useState<Record<string, Card>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadBinderData() {
      if (!profile) {
        setBinder(undefined);
        setEntries([]);
        setCardsById({});
        setLoading(false);
        return;
      }

      setLoading(true);
      const nextBinder = await getBinderById(binderId, profile.id);
      setBinder(nextBinder);

      const binderEntries = await getCollectionEntries(profile.id, binderId);
      setEntries(binderEntries);

      const uniqueCardIds = [...new Set(binderEntries.map((entry) => entry.cardId))];
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

    void loadBinderData();
  }, [binderId, profile]);

  async function handleDelete(entryId: string) {
    await deleteCollectionEntry(entryId);
    setEntries((current) => current.filter((entry) => entry.id !== entryId));
  }

  return (
    <ScreenLayout
      title={binder?.name ?? "Binder Detail"}
      subtitle={binder?.description ?? "Cards currently assigned to this binder."}
    >
      {loading ? <LoadingState label="Loading binder..." /> : null}
      {!loading && entries.length === 0 ? (
        <EmptyState
          title="No cards here yet"
          message="Add a card to this binder from the card detail screen."
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
