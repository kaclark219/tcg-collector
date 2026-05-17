import { useEffect, useState } from "react";
import { router } from "expo-router";
import { StyleSheet, View, useWindowDimensions } from "react-native";
import { CardTile } from "@/components/CardTile";
import { EmptyState } from "@/components/EmptyState";
import { SearchBar } from "@/components/SearchBar";
import { ScreenLayout } from "@/screens/shared";
import { searchCards } from "@/services/cardsApi";
import { Card } from "@/types";

export function SearchScreen() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Card[]>([]);
  const { width } = useWindowDimensions();

  const columns = width >= 1080 ? 3 : 2;
  const cardWidth = columns === 3 ? "31.5%" : "48.2%";

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
      <View style={styles.grid}>
        {results.map((card) => (
          <CardTile
            key={card.id}
            card={card}
            compact
            style={{ width: cardWidth }}
            onPress={() => router.push(`/cards/${card.id}`)}
          />
        ))}
      </View>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
    alignItems: "flex-start",
  },
});
