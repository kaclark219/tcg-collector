import { useState } from "react";
import { router } from "expo-router";
import { Pressable, StyleSheet, Text } from "react-native";
import { LoadingState } from "@/components/LoadingState";
import { ScreenLayout } from "@/screens/shared";
import { simulateScan } from "@/services/scanApi";

export function ScanScreen() {
  const [loading, setLoading] = useState(false);

  async function handleSimulateScan() {
    setLoading(true);
    const session = await simulateScan();
    setLoading(false);
    router.push(`/scan/results/${session.id}`);
  }

  return (
    <ScreenLayout
      title="Scan"
      subtitle="Placeholder screen. Real camera, crop, OCR, and ranking will plug in here later."
    >
      <Pressable style={styles.button} onPress={handleSimulateScan}>
        <Text style={styles.buttonText}>Simulate Scan</Text>
      </Pressable>
      {loading ? <LoadingState label="Generating mock scan candidates..." /> : null}
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  button: {
    alignSelf: "flex-start",
    paddingHorizontal: 18,
    paddingVertical: 14,
    borderRadius: 999,
    backgroundColor: "#b53f1e",
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700",
  },
});

