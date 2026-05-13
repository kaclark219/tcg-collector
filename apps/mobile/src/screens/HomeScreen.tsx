import { router } from "expo-router";
import { Pressable, StyleSheet, Text } from "react-native";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";

const links = [
  { href: "/collection", label: "Collection" },
  { href: "/binders", label: "Binders" },
  { href: "/search", label: "Search" },
  { href: "/scan", label: "Scan" },
  { href: "/settings", label: "Settings" },
] as const;

export function HomeScreen() {
  const { profile, setProfile } = useAuth();

  return (
    <ScreenLayout
      title="Pokemon Card Collector"
      subtitle={`Signed in as ${profile?.username ?? "guest"}. Manual tracking first, scan-assisted identification later.`}
    >
      <Pressable style={styles.logoutButton} onPress={() => setProfile(null)}>
        <Text style={styles.logoutText}>Log Out</Text>
      </Pressable>
      {links.map((link) => (
        <Pressable
          key={link.href}
          style={styles.linkCard}
          onPress={() => router.push(link.href)}
        >
          <Text style={styles.linkLabel}>{link.label}</Text>
          <Text style={styles.linkHint}>Open {link.label.toLowerCase()}</Text>
        </Pressable>
      ))}
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  linkCard: {
    padding: 18,
    borderRadius: 20,
    backgroundColor: "#fffefb",
    borderWidth: 1,
    borderColor: "#e7d8c7",
    gap: 4,
  },
  linkLabel: {
    fontSize: 18,
    fontWeight: "700",
    color: "#513326",
  },
  linkHint: {
    color: "#7a6658",
  },
  logoutButton: {
    alignSelf: "flex-start",
    backgroundColor: "#ead6c4",
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  logoutText: {
    color: "#5d3c2b",
    fontWeight: "700",
  },
});
