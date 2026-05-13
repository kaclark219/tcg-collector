import { Stack } from "expo-router";
import { AuthProvider } from "@/context/AuthContext";

export default function RootLayout() {
  return (
    <AuthProvider>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: "#f7f0e8",
          },
          headerTintColor: "#42281e",
          contentStyle: {
            backgroundColor: "#f7f0e8",
          },
          headerBackButtonDisplayMode: "minimal",
        }}
      >
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="collection" options={{ headerShown: false }} />
        <Stack.Screen name="binders/index" options={{ headerShown: false }} />
        <Stack.Screen name="search" options={{ headerShown: false }} />
        <Stack.Screen name="scan/index" options={{ headerShown: false }} />
        <Stack.Screen name="settings" options={{ headerShown: false }} />

        <Stack.Screen
          name="binders/[binderId]"
          options={{
            title: "Binder",
          }}
        />
        <Stack.Screen
          name="cards/[cardId]"
          options={{
            title: "Card",
          }}
        />
        <Stack.Screen
          name="add-to-collection"
          options={{
            title: "Add To Collection",
          }}
        />
        <Stack.Screen
          name="scan/results/[scanId]"
          options={{
            title: "Scan Results",
          }}
        />
      </Stack>
    </AuthProvider>
  );
}
