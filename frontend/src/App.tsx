import { AuthScreen } from "./components/AuthScreen";
import { AppShell } from "./components/AppShell";
import { useAppStore } from "./store/app-store";

export default function App() {
  const token = useAppStore((state) => state.token);

  return token ? <AppShell /> : <AuthScreen />;
}
