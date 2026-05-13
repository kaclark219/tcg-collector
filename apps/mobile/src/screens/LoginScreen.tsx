import { useState } from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";
import { useAuth } from "@/context/AuthContext";
import { ScreenLayout } from "@/screens/shared";
import { loginProfile } from "@/services/authApi";

export function LoginScreen() {
  const { setProfile } = useAuth();
  const [username, setUsername] = useState("mygblvsh");
  const [pin, setPin] = useState("021903");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleLogin() {
    setSubmitting(true);
    setError(null);

    try {
      const response = await loginProfile(username, pin);
      setProfile(response.profile);
    } catch (error) {
      if (error instanceof Error) {
        setError(`Login failed. ${error.message}`);
      } else {
        setError("Login failed. Check the username, PIN, and API server.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <ScreenLayout
      title="Login"
      subtitle="Use your local profile username and six-digit PIN."
    >
      <View style={styles.fieldGroup}>
        <Text style={styles.label}>Username</Text>
        <TextInput
          autoCapitalize="none"
          value={username}
          onChangeText={setUsername}
          style={styles.input}
        />
      </View>
      <View style={styles.fieldGroup}>
        <Text style={styles.label}>PIN</Text>
        <TextInput
          value={pin}
          onChangeText={setPin}
          keyboardType="number-pad"
          maxLength={6}
          secureTextEntry
          style={styles.input}
        />
      </View>
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Pressable style={styles.button} onPress={handleLogin} disabled={submitting}>
        <Text style={styles.buttonText}>
          {submitting ? "Logging In..." : "Log In"}
        </Text>
      </Pressable>
    </ScreenLayout>
  );
}

const styles = StyleSheet.create({
  fieldGroup: {
    gap: 8,
  },
  label: {
    fontSize: 14,
    fontWeight: "700",
    color: "#5d3d2b",
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
  error: {
    color: "#a93020",
  },
  button: {
    alignSelf: "flex-start",
    paddingHorizontal: 18,
    paddingVertical: 14,
    borderRadius: 999,
    backgroundColor: "#b53f1e",
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700",
  },
});
