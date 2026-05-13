import { useLocalSearchParams } from "expo-router";
import { ScanResultScreen } from "@/screens/ScanResultScreen";

export default function ScanResultRoute() {
  const params = useLocalSearchParams<{ scanId: string }>();

  return <ScanResultScreen scanId={params.scanId} />;
}

