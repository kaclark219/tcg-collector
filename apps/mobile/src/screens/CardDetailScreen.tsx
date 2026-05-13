import { router } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { CardImage } from "@/components/CardImage";
import { ScreenLayout } from "@/screens/shared";
import { Card } from "@/types";

type CardDetailScreenProps = {
  card?: Card;
};

export function CardDetailScreen({ card }: CardDetailScreenProps) {
  return (
    <ScreenLayout
      title={card?.name ?? "Card Detail"}
      subtitle="Master card record placeholder. Real catalog metadata can be expanded later."
    >
      <View style={styles.detailRow}>
        <CardImage
          imageUrl={card?.imageUrl}
          style={styles.image}
          placeholderStyle={styles.imagePlaceholder}
          resizeMode="contain"
        />
        <View style={styles.box}>
          <Text style={styles.label}>Set</Text>
          <Text style={styles.value}>{card?.setName ?? "Unknown set"}</Text>
          <Text style={styles.label}>Number</Text>
          <Text style={styles.value}>{card?.number ?? "Unknown number"}</Text>
          <Text style={styles.label}>Rarity</Text>
          <Text style={styles.value}>{card?.rarity ?? "Unknown rarity"}</Text>
        </View>
      </View>
      <Pressable
        style={styles.button}
        onPress={() =>
          router.push(card ? `/add-to-collection?cardId=${card.id}` : "/add-to-collection")
        }
      >
        <Text style={styles.buttonText}>Add to Collection</Text>
      </Pressable>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  detailRow: {
    flexDirection: "row",
    gap: 16,
    alignItems: "stretch",
  },
  image: {
    flex: 1,
    height: 320,
    borderRadius: 18,
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e4d8c9",
  },
  imagePlaceholder: {
    flex: 1,
    height: 320,
    borderRadius: 18,
    backgroundColor: "#f0e1cf",
    borderWidth: 1,
    borderColor: "#e4d8c9",
    alignItems: "center",
    justifyContent: "center",
  },
  box: {
    flex: 1,
    padding: 18,
    borderRadius: 18,
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e4d8c9",
    gap: 8,
  },
  label: {
    fontSize: 13,
    textTransform: "uppercase",
    letterSpacing: 0.4,
    color: "#9c6d46",
  },
  value: {
    fontSize: 18,
    color: "#4e3023",
    marginBottom: 4,
  },
  button: {
    backgroundColor: "#b53f1e",
    borderRadius: 999,
    paddingHorizontal: 18,
    paddingVertical: 14,
    alignSelf: "flex-start",
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700",
  },
});
