import { Pressable, StyleSheet, Text, View } from "react-native";
import { Card, ScanCandidate } from "@/types";

type CandidateMatchCardProps = {
  candidate: ScanCandidate;
  card?: Card;
  onConfirm?: () => void;
};

export function CandidateMatchCard({
  candidate,
  card,
  onConfirm,
}: CandidateMatchCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.name}>{card?.name ?? candidate.cardId}</Text>
      <Text style={styles.meta}>
        Confidence: {Math.round(candidate.confidence * 100)}%
      </Text>
      <Text style={styles.reason}>{candidate.reason}</Text>
      <Pressable style={styles.button} onPress={onConfirm}>
        <Text style={styles.buttonText}>Confirm Placeholder</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    backgroundColor: "#fffefb",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#e4d8c9",
    gap: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: "700",
    color: "#513426",
  },
  meta: {
    color: "#8a4621",
    fontWeight: "600",
  },
  reason: {
    color: "#6d594b",
  },
  button: {
    alignSelf: "flex-start",
    backgroundColor: "#b53f1e",
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700",
  },
});

