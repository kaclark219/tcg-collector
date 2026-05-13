import { StyleSheet, Text, View } from "react-native";

type EmptyStateProps = {
  title: string;
  message: string;
};

export function EmptyState({ title, message }: EmptyStateProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    borderRadius: 16,
    backgroundColor: "#fff6eb",
    borderWidth: 1,
    borderColor: "#f0d0a5",
    gap: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: "700",
    color: "#6d3b1f",
  },
  message: {
    fontSize: 14,
    color: "#7a6758",
  },
});

