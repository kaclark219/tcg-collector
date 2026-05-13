import { useAuth } from "@/context/AuthContext";
import { HomeScreen } from "@/screens/HomeScreen";
import { LoginScreen } from "@/screens/LoginScreen";

export default function IndexRoute() {
  const { profile } = useAuth();

  return profile ? <HomeScreen /> : <LoginScreen />;
}
