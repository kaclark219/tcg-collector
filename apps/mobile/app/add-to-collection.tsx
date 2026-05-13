import { useLocalSearchParams } from "expo-router";
import { AddToCollectionScreen } from "@/screens/AddToCollectionScreen";

export default function AddToCollectionRoute() {
  const params = useLocalSearchParams<{ cardId?: string }>();

  return <AddToCollectionScreen cardId={params.cardId} />;
}
