import { useEffect } from "react";
import { AuthScreen } from "./components/AuthScreen";
import { AppShell } from "./components/AppShell";
import { useAppStore } from "./store/app-store";

export default function App() {
  const token = useAppStore((state) => state.token);
  const theme = useAppStore((state) => state.theme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  return token ? <AppShell /> : <AuthScreen />;
}
