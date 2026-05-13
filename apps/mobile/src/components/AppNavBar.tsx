import { router, usePathname } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useAuth } from "@/context/AuthContext";

const navItems = [
  { href: "/", label: "Home", match: "/" },
  { href: "/collection", label: "Collection", match: "/collection" },
  { href: "/binders", label: "Binders", match: "/binders" },
  { href: "/search", label: "Search", match: "/search" },
  { href: "/scan", label: "Scan", match: "/scan" },
] as const;

export function AppNavBar() {
  const pathname = usePathname();
  const { profile } = useAuth();

  if (!profile) {
    return null;
  }

  return (
    <View style={styles.wrap}>
      <View style={styles.bar}>
        {navItems.map((item) => {
          const isActive =
            item.match === "/"
              ? pathname === "/"
              : pathname === item.match || pathname.startsWith(`${item.match}/`);

          return (
            <Pressable
              key={item.href}
              style={[styles.item, isActive ? styles.itemActive : null]}
              onPress={() => router.push(item.href)}
            >
              <Text style={[styles.label, isActive ? styles.labelActive : null]}>
                {item.label}
              </Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    paddingHorizontal: 12,
    paddingBottom: 12,
    paddingTop: 6,
    backgroundColor: "#f7f0e8",
  },
  bar: {
    flexDirection: "row",
    backgroundColor: "#fffefb",
    borderRadius: 22,
    borderWidth: 1,
    borderColor: "#e4d8c9",
    padding: 6,
    gap: 6,
  },
  item: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 16,
    paddingVertical: 10,
    paddingHorizontal: 8,
  },
  itemActive: {
    backgroundColor: "#b53f1e",
  },
  label: {
    fontSize: 12,
    fontWeight: "700",
    color: "#6b4d3b",
  },
  labelActive: {
    color: "#ffffff",
  },
});
