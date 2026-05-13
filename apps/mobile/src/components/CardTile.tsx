import { Pressable, StyleSheet, Text, View } from "react-native";
import { CardImage } from "@/components/CardImage";
import { Card } from "@/types";

type CardTileProps = {
  card: Card;
  onPress?: () => void;
};

export function CardTile({ card, onPress }: CardTileProps) {
  return (
    <Pressable style={styles.card} onPress={onPress}>
      <CardImage
        imageUrl={card.imageUrl}
        style={styles.thumbnail}
        placeholderStyle={styles.thumbnailPlaceholder}
        resizeMode="cover"
      />
      <View style={styles.content}>
        <Text style={styles.name}>{card.name}</Text>
        <Text style={styles.meta}>{card.setName}</Text>
        <Text style={styles.meta}>
          {card.number} • {card.rarity}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    gap: 14,
    backgroundColor: "#ffffff",
    borderRadius: 18,
    padding: 14,
    borderWidth: 1,
    borderColor: "#e4d8c9",
  },
  thumbnail: {
    width: 56,
    height: 80,
    borderRadius: 12,
    backgroundColor: "#fff8f0",
    borderWidth: 1,
    borderColor: "#ead8c2",
  },
  thumbnailPlaceholder: {
    width: 56,
    height: 80,
    borderRadius: 12,
    backgroundColor: "#ffd07a",
  },
  content: {
    flex: 1,
    gap: 4,
    justifyContent: "center",
  },
  name: {
    fontSize: 17,
    fontWeight: "700",
    color: "#40291f",
  },
  meta: {
    fontSize: 14,
    color: "#755f52",
  },
});
