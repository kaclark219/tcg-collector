import { ActivityIndicator, StyleSheet, Text, View } from "react-native";

type LoadingStateProps = {
  label?: string;
};

export function LoadingState({ label = "Loading..." }: LoadingStateProps) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="small" color="#b53f1e" />
      <Text style={styles.label}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingVertical: 24,
  },
  label: {
    color: "#5a4a3b",
    fontSize: 15,
  },
});

