import { Pressable, StyleSheet, Text, View } from "react-native";
import { CardImage } from "@/components/CardImage";
import { Card, CollectionEntry } from "@/types";

type CollectionEntryCardProps = {
  entry: CollectionEntry;
  card?: Card;
  onDelete?: () => void;
};

export function CollectionEntryCard({
  entry,
  card,
  onDelete,
}: CollectionEntryCardProps) {
  return (
    <View style={styles.card}>
      <View style={styles.row}>
        <CardImage
          imageUrl={card?.imageUrl}
          style={styles.thumbnail}
          placeholderStyle={styles.thumbnailPlaceholder}
          resizeMode="cover"
        />
        <View style={styles.content}>
          <View style={styles.titleRow}>
            <Text style={styles.title}>{card?.name ?? entry.cardId}</Text>
            {onDelete ? (
              <Pressable style={styles.deleteButton} onPress={onDelete}>
                <Text style={styles.deleteButtonText}>🗑</Text>
              </Pressable>
            ) : null}
          </View>
          <Text style={styles.meta}>{card?.setName ?? "Unknown set"}</Text>
          <Text style={styles.meta}>Variant: {entry.variant}</Text>
          {entry.notes ? <Text style={styles.meta}>Notes: {entry.notes}</Text> : null}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    backgroundColor: "#ffffff",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#e4d8c9",
  },
  row: {
    flexDirection: "row",
    gap: 12,
  },
  thumbnail: {
    width: 64,
    height: 92,
    borderRadius: 10,
    backgroundColor: "#fff8f0",
    borderWidth: 1,
    borderColor: "#ead8c2",
  },
  thumbnailPlaceholder: {
    width: 64,
    height: 92,
    borderRadius: 10,
    backgroundColor: "#ffd07a",
  },
  content: {
    flex: 1,
    gap: 6,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: "700",
    color: "#503323",
    flex: 1,
  },
  meta: {
    color: "#705b4e",
  },
  deleteButton: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f6d8d2",
    borderWidth: 1,
    borderColor: "#e3b5ab",
  },
  deleteButtonText: {
    fontSize: 16,
  },
});
