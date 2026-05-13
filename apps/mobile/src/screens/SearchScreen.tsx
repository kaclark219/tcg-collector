import { useEffect, useState } from "react";
import { router } from "expo-router";
import { CardTile } from "@/components/CardTile";
import { EmptyState } from "@/components/EmptyState";
import { SearchBar } from "@/components/SearchBar";
import { ScreenLayout } from "@/screens/shared";
import { searchCards } from "@/services/cardsApi";
import { Card } from "@/types";

export function SearchScreen() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Card[]>([]);

  useEffect(() => {
    searchCards(query).then(setResults);
  }, [query]);

  return (
    <ScreenLayout
      title="Search"
      subtitle="Manual search comes first so collection flows can work before scan logic exists."
    >
      <SearchBar value={query} onChangeText={setQuery} />
      {results.length === 0 ? (
        <EmptyState
          title="No matches"
          message="Try a card name, set, or collector number."
        />
      ) : null}
      {results.map((card) => (
        <CardTile
          key={card.id}
          card={card}
          onPress={() => router.push(`/cards/${card.id}`)}
        />
      ))}
    </ScreenLayout>
  );
}
