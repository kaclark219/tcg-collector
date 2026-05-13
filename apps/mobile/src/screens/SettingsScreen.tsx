import { EmptyState } from "@/components/EmptyState";
import { ScreenLayout } from "@/screens/shared";

export function SettingsScreen() {
  return (
    <ScreenLayout
      title="Settings"
      subtitle="Placeholder for API base URL, import preferences, and account settings later."
    >
      <EmptyState
        title="Settings coming later"
        message="TODO: decide when auth, sync settings, and offline behavior should enter the roadmap."
      />
    </ScreenLayout>
  );
}

