import { Pressable, StyleSheet, Text, View } from "react-native";
import { Binder } from "@/types";

type BinderCardProps = {
  binder: Binder;
  onPress?: () => void;
};

export function BinderCard({ binder, onPress }: BinderCardProps) {
  return (
    <Pressable style={styles.card} onPress={onPress}>
      <View>
        <Text style={styles.name}>{binder.name}</Text>
        <Text style={styles.description}>
          {binder.description ?? "No description yet."}
        </Text>
      </View>
      <Text style={styles.count}>{binder.entryCount} entries</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e4d8c9",
    borderRadius: 18,
    padding: 16,
    gap: 10,
  },
  name: {
    fontSize: 18,
    fontWeight: "700",
    color: "#503323",
  },
  description: {
    color: "#725d51",
    marginTop: 4,
  },
  count: {
    color: "#b04b1f",
    fontWeight: "600",
  },
});

