import { useEffect, useState } from "react";
import { router } from "expo-router";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { BinderCard } from "@/components/BinderCard";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";
import { createBinder, getBinders } from "@/services/bindersApi";
import { Binder } from "@/types";

export function BinderListScreen() {
  const { profile } = useAuth();
  const [binders, setBinders] = useState<Binder[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function loadBinders() {
    if (!profile) {
      setBinders([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    const nextBinders = await getBinders(profile.id);
    setBinders(nextBinders);
    setLoading(false);
  }

  useEffect(() => {
    void loadBinders();
  }, [profile]);

  async function handleCreateBinder() {
    if (!profile) {
      return;
    }

    setCreating(true);
    setError(null);

    try {
      const binder = await createBinder(profile.id, name, description);
      setBinders((current) => [...current, binder]);
      setName("");
      setDescription("");
    } catch {
      setError("Unable to create binder right now.");
    } finally {
      setCreating(false);
    }
  }

  return (
    <ScreenLayout
      title="Binders"
      subtitle="User-created groups for organizing collection entries."
    >
      <View style={styles.formCard}>
        <Text style={styles.formTitle}>Create Binder</Text>
        <TextInput
          value={name}
          onChangeText={setName}
          placeholder="Binder name"
          style={styles.input}
        />
        <TextInput
          value={description}
          onChangeText={setDescription}
          placeholder="Optional description"
          style={styles.input}
        />
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Pressable style={styles.button} onPress={handleCreateBinder} disabled={creating}>
          <Text style={styles.buttonText}>
            {creating ? "Creating..." : "Create Binder"}
          </Text>
        </Pressable>
      </View>
      {loading ? <LoadingState label="Loading binders..." /> : null}
      {!loading && binders.length === 0 ? (
        <EmptyState
          title="No binders yet"
          message="Create a binder once you decide how you want organization to work."
        />
      ) : null}
      {binders.map((binder) => (
        <BinderCard
          key={binder.id}
          binder={binder}
          onPress={() => router.push(`/binders/${binder.id}`)}
        />
      ))}
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  formCard: {
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e4d8c9",
    borderRadius: 18,
    padding: 16,
    gap: 10,
  },
  formTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#503323",
  },
  input: {
    backgroundColor: "#ffffff",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#e2d7cc",
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
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
  error: {
    color: "#a93020",
  },
});
