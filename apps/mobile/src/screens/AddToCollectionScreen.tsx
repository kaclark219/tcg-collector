import { useEffect, useState } from "react";
import { router } from "expo-router";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";
import { getBinders } from "@/services/bindersApi";
import { getCardById } from "@/services/cardsApi";
import { createCollectionEntry } from "@/services/collectionApi";
import { Binder, Card } from "@/types";

type AddToCollectionScreenProps = {
  cardId?: string;
};

function getAvailableVariantOptions(card?: Card): string[] {
  if (!card) {
    return ["unknown"];
  }

  const options: string[] = [];
  if (card.variantNormal) {
    options.push("normal");
  }
  if (card.variantReverse) {
    options.push("reverse");
  }
  if (card.variantHolo) {
    options.push("holo");
  }
  if (card.variantFirstEdition) {
    options.push("first_edition");
  }
  if (card.variantWPromo) {
    options.push("w_promo");
  }

  return options.length > 0 ? options : ["unknown"];
}

export function AddToCollectionScreen({ cardId }: AddToCollectionScreenProps) {
  const { profile } = useAuth();
  const [card, setCard] = useState<Card | undefined>();
  const [binders, setBinders] = useState<Binder[]>([]);
  const [selectedBinderId, setSelectedBinderId] = useState("");
  const [variant, setVariant] = useState("unknown");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadForm() {
      if (!profile || !cardId) {
        setLoading(false);
        return;
      }

      setLoading(true);
      const [loadedCard, loadedBinders] = await Promise.all([
        getCardById(cardId),
        getBinders(profile.id),
      ]);
      setCard(loadedCard);
      setBinders(loadedBinders);
      setSelectedBinderId(loadedBinders[0]?.id ?? "");
      setVariant(getAvailableVariantOptions(loadedCard)[0] ?? "unknown");
      setLoading(false);
    }

    void loadForm();
  }, [profile, cardId]);

  async function handleAdd() {
    if (!profile || !cardId || !selectedBinderId) {
      setError("A profile, card, and binder are required.");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await createCollectionEntry({
        profileId: profile.id,
        cardId,
        binderId: selectedBinderId,
        variant,
        notes,
      });
      router.push("/collection");
    } catch {
      setError("Unable to add this card to your collection right now.");
    } finally {
      setSubmitting(false);
    }
  }

  if (!cardId) {
    return (
      <ScreenLayout title="Add To Collection" subtitle="No card was selected.">
        <EmptyState
          title="Missing card"
          message="Open a card detail screen first, then choose Add to Collection."
        />
      </ScreenLayout>
    );
  }

  return (
    <ScreenLayout
      title="Add To Collection"
      subtitle="Create one real collection entry for this physical card."
    >
      {loading ? <LoadingState label="Loading add form..." /> : null}
      {!loading && card ? (
        <View style={styles.cardBox}>
          <Text style={styles.cardName}>{card.name}</Text>
          <Text style={styles.cardMeta}>
            {card.setName} • {card.number}
          </Text>
        </View>
      ) : null}
      {!loading && binders.length === 0 ? (
        <EmptyState
          title="No binders available"
          message="Create a binder first, or log in again so the fallback binder is available."
        />
      ) : null}
      {!loading && binders.length > 0 ? (
        <View style={styles.form}>
          <Text style={styles.label}>Binder</Text>
          <View style={styles.optionList}>
            {binders.map((binder) => (
              <Pressable
                key={binder.id}
                style={[
                  styles.optionChip,
                  selectedBinderId === binder.id ? styles.optionChipSelected : null,
                ]}
                onPress={() => setSelectedBinderId(binder.id)}
              >
                <Text
                  style={[
                    styles.optionChipText,
                    selectedBinderId === binder.id ? styles.optionChipTextSelected : null,
                  ]}
                >
                  {binder.name}
                </Text>
              </Pressable>
            ))}
          </View>
          <Text style={styles.label}>Variant</Text>
          <View style={styles.optionList}>
            {getAvailableVariantOptions(card).map((option) => (
              <Pressable
                key={option}
                style={[
                  styles.optionChip,
                  variant === option ? styles.optionChipSelected : null,
                ]}
                onPress={() => setVariant(option)}
              >
                <Text
                  style={[
                    styles.optionChipText,
                    variant === option ? styles.optionChipTextSelected : null,
                  ]}
                >
                  {option}
                </Text>
              </Pressable>
            ))}
          </View>
          <Text style={styles.label}>Notes</Text>
          <TextInput
            value={notes}
            onChangeText={setNotes}
            placeholder="Optional notes"
            style={styles.input}
            multiline
          />
          {error ? <Text style={styles.error}>{error}</Text> : null}
          <Pressable style={styles.button} onPress={handleAdd} disabled={submitting}>
            <Text style={styles.buttonText}>
              {submitting ? "Adding..." : "Add To Collection"}
            </Text>
          </Pressable>
        </View>
      ) : null}
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  cardBox: {
    padding: 16,
    borderRadius: 18,
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e4d8c9",
    gap: 4,
  },
  cardName: {
    fontSize: 18,
    fontWeight: "700",
    color: "#503323",
  },
  cardMeta: {
    color: "#705b4e",
  },
  form: {
    gap: 12,
  },
  label: {
    fontSize: 14,
    fontWeight: "700",
    color: "#5d3d2b",
  },
  optionList: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
  },
  optionChip: {
    borderRadius: 999,
    borderWidth: 1,
    borderColor: "#d8c3af",
    backgroundColor: "#fffefb",
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  optionChipSelected: {
    backgroundColor: "#b53f1e",
    borderColor: "#b53f1e",
  },
  optionChipText: {
    color: "#6b4d3b",
    fontWeight: "600",
  },
  optionChipTextSelected: {
    color: "#ffffff",
  },
  input: {
    backgroundColor: "#ffffff",
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#e2d7cc",
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
    minHeight: 90,
    textAlignVertical: "top",
  },
  button: {
    alignSelf: "flex-start",
    backgroundColor: "#b53f1e",
    borderRadius: 999,
    paddingHorizontal: 18,
    paddingVertical: 14,
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700",
  },
  error: {
    color: "#a93020",
  },
});
