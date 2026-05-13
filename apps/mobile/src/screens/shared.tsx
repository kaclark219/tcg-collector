import { PropsWithChildren } from "react";
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from "react-native";
import { AppNavBar } from "@/components/AppNavBar";

export function ScreenLayout({
  title,
  subtitle,
  children,
}: PropsWithChildren<{ title: string; subtitle?: string }>) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.body}>
        <ScrollView contentContainerStyle={styles.content}>
          <View style={styles.header}>
            <Text style={styles.title}>{title}</Text>
            {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
          </View>
          {children}
        </ScrollView>
      </View>
      <AppNavBar />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#f7f0e8",
  },
  body: {
    flex: 1,
  },
  content: {
    padding: 20,
    gap: 14,
  },
  header: {
    gap: 6,
    marginBottom: 8,
  },
  title: {
    fontSize: 32,
    fontWeight: "800",
    color: "#41271d",
  },
  subtitle: {
    color: "#6d594b",
    fontSize: 15,
    lineHeight: 22,
  },
});
