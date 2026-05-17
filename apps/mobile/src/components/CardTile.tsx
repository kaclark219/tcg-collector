import { Pressable, StyleProp, StyleSheet, Text, View, ViewStyle } from "react-native";
import { CardImage } from "@/components/CardImage";
import { Card } from "@/types";

type CardTileProps = {
  card: Card;
  onPress?: () => void;
  compact?: boolean;
  style?: StyleProp<ViewStyle>;
};

export function CardTile({ card, onPress, compact = false, style }: CardTileProps) {
  return (
    <Pressable
      style={[styles.card, compact ? styles.cardCompact : null, style]}
      onPress={onPress}
    >
      <CardImage
        imageUrl={card.imageUrl}
        style={compact ? styles.thumbnailCompact : styles.thumbnail}
        placeholderStyle={compact ? styles.thumbnailPlaceholderCompact : styles.thumbnailPlaceholder}
        resizeMode={compact ? "contain" : "cover"}
      />
      <View style={[styles.content, compact ? styles.contentCompact : null]}>
        <Text style={[styles.name, compact ? styles.nameCompact : null]} numberOfLines={2}>
          {card.name}
        </Text>
        <Text style={[styles.meta, compact ? styles.metaCompact : null]} numberOfLines={2}>
          {card.setName}
        </Text>
        <Text style={[styles.meta, compact ? styles.metaCompact : null]} numberOfLines={1}>
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
  cardCompact: {
    flexDirection: "column",
    gap: 10,
    padding: 12,
    maxWidth: 220,
  },
  thumbnail: {
    width: 56,
    height: 80,
    borderRadius: 12,
    backgroundColor: "#fff8f0",
    borderWidth: 1,
    borderColor: "#ead8c2",
  },
  thumbnailCompact: {
    width: "100%",
    aspectRatio: 0.72,
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
  thumbnailPlaceholderCompact: {
    width: "100%",
    aspectRatio: 0.72,
    borderRadius: 12,
    backgroundColor: "#ffd07a",
  },
  content: {
    flex: 1,
    gap: 4,
    justifyContent: "center",
  },
  contentCompact: {
    gap: 6,
    justifyContent: "flex-start",
  },
  name: {
    fontSize: 17,
    fontWeight: "700",
    color: "#40291f",
  },
  nameCompact: {
    fontSize: 15,
    lineHeight: 20,
  },
  meta: {
    fontSize: 14,
    color: "#755f52",
  },
  metaCompact: {
    fontSize: 12,
    lineHeight: 16,
  },
});
