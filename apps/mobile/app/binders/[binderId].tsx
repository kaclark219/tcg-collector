import { useLocalSearchParams } from "expo-router";
import { BinderDetailScreen } from "@/screens/BinderDetailScreen";

export default function BinderDetailRoute() {
  const params = useLocalSearchParams<{ binderId: string }>();

  return <BinderDetailScreen binderId={params.binderId} />;
}

