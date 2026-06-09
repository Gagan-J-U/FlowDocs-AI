import { FormEvent, useState } from "react";
import { motion } from "framer-motion";
import { BrainCircuit, LockKeyhole, Moon, Sparkles, Sun } from "lucide-react";
import { api } from "../lib/api";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { useAppStore } from "../store/app-store";

export function AuthScreen() {
  const { setToken, setTheme, theme } = useAppStore();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === "register") {
        await api.register({ username, email, password });
      }

      const response = await api.login({ email, password });
      setToken(response.access_token);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center px-4 py-8">
      <motion.section
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid w-full max-w-5xl overflow-hidden rounded-2xl border border-line/80 bg-panel/80 shadow-panel backdrop-blur-2xl md:grid-cols-[1.05fr_0.95fr] dark:border-white/10 dark:bg-ink/70"
      >
        <div className="relative min-h-[520px] border-b border-line p-8 md:border-b-0 md:border-r">
          <div className="relative flex h-full flex-col justify-between">
            <div>
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-brand/30 bg-brand/15">
                <BrainCircuit className="h-6 w-6 text-brand" />
              </div>
              <h1 className="mt-8 max-w-md text-4xl font-semibold tracking-normal text-foreground">
                FlowDocs AI
              </h1>
              <p className="mt-4 max-w-md text-base leading-7 text-muted">
                Collaborative document intelligence for research teams.
              </p>
            </div>
            <div className="grid gap-3 text-sm text-muted dark:text-slate-300">
              <div className="glass rounded-xl p-4">
                <Sparkles className="mb-3 h-5 w-5 text-mint" />
                Hybrid retrieval, reranking, and prompt modes stay behind one focused research surface.
              </div>
              <div className="glass rounded-xl p-4">
                <LockKeyhole className="mb-3 h-5 w-5 text-brand" />
                JWT sessions and workspace-scoped data keep document brains isolated.
              </div>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-8">
          <div className="mb-8 flex items-start justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.22em] text-brand/80">
                {mode === "login" ? "Welcome back" : "Create account"}
              </p>
              <h2 className="mt-2 text-2xl font-semibold text-foreground dark:text-white">
                {mode === "login" ? "Open your workspace" : "Start a workspace"}
              </h2>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
          </div>

          <div className="grid gap-4">
            {mode === "register" && (
              <label className="grid gap-2 text-sm text-muted dark:text-slate-300">
                Username
                <Input value={username} onChange={(event) => setUsername(event.target.value)} required />
              </label>
            )}
            <label className="grid gap-2 text-sm text-muted dark:text-slate-300">
              Email
              <Input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </label>
            <label className="grid gap-2 text-sm text-muted dark:text-slate-300">
              Password
              <Input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            </label>
          </div>

          {error && (
            <div className="mt-4 rounded-lg border border-red-400/25 bg-red-500/10 px-3 py-2 text-sm text-red-700 dark:text-red-100">
              {error}
            </div>
          )}

          <Button type="submit" variant="primary" className="mt-6 w-full" disabled={loading}>
            {loading ? "Working..." : mode === "login" ? "Login" : "Register"}
          </Button>

          <button
            type="button"
            onClick={() => setMode(mode === "login" ? "register" : "login")}
            className="mt-5 w-full text-sm text-muted transition hover:text-foreground dark:text-slate-400 dark:hover:text-white"
          >
            {mode === "login" ? "Need an account? Register" : "Already have an account? Login"}
          </button>
        </form>
      </motion.section>
    </main>
  );
}
