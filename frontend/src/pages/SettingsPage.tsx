import { FormEvent, useEffect, useState } from "react";
import { Github, Globe, Linkedin, Palette, Shield, UserRound } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { ResearchProfile, Theme } from "../types";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { ErrorState } from "../components/ui/empty-state";
import { SkeletonText } from "../components/ui/skeleton";

type SettingsTab = "profile" | "appearance" | "research" | "privacy" | "accounts";

export function SettingsPage() {
  const { token, theme, setTheme, user } = useAppStore();
  const [tab, setTab] = useState<SettingsTab>("profile");
  const [profile, setProfile] = useState<ResearchProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  const [form, setForm] = useState({
    bio: "",
    institution: "",
    department: "",
    skills: "",
    interests: "",
    github_url: "",
    linkedin_url: "",
    website_url: "",
    visibility: "public",
  });

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    void api.researchProfile(token)
      .then((data) => {
        setProfile(data);
        setForm({
          bio: data.bio ?? "",
          institution: data.institution ?? "",
          department: data.department ?? "",
          skills: data.skills ?? "",
          interests: data.interests ?? "",
          github_url: data.github_url ?? "",
          linkedin_url: data.linkedin_url ?? "",
          website_url: data.website_url ?? "",
          visibility: data.visibility ?? "public",
        });
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load profile"))
      .finally(() => setLoading(false));
  }, [token]);

  async function saveResearchProfile(event: FormEvent) {
    event.preventDefault();
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const updated = await api.updateResearchProfile(token, form);
      setProfile(updated);
      setSaved(true);
      window.setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setLoading(false);
    }
  }

  const tabs: { id: SettingsTab; label: string; icon: typeof UserRound }[] = [
    { id: "profile", label: "Profile", icon: UserRound },
    { id: "appearance", label: "Appearance", icon: Palette },
    { id: "research", label: "Research profile", icon: Globe },
    { id: "privacy", label: "Privacy", icon: Shield },
    { id: "accounts", label: "Connected accounts", icon: Github },
  ];

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 lg:flex-row">
        <aside className="lg:w-56">
          <h1 className="text-2xl font-semibold text-foreground">Settings</h1>
          <nav className="mt-4 grid gap-1">
            {tabs.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setTab(id)}
                className={`flex items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition ${
                  tab === id ? "bg-brand/10 text-brand" : "text-muted hover:bg-subtle/40"
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            ))}
          </nav>
        </aside>

        <section className="min-w-0 flex-1 rounded-2xl border border-line bg-panel p-5">
          {tab === "profile" && (
            <div>
              <h2 className="text-lg font-semibold text-foreground">Profile settings</h2>
              <p className="mt-1 text-sm text-muted">Manage your account identity within FlowDocs.</p>
              <div className="mt-6 grid gap-3">
                 <Input placeholder="Display name" value={user?.username ?? ""} disabled />
                 <Input placeholder="Email" value={user?.email ?? ""} disabled />
              </div>
            </div>
          )}

          {tab === "appearance" && (
            <div>
              <h2 className="text-lg font-semibold text-foreground">Appearance</h2>
              <p className="mt-1 text-sm text-muted">Choose light or dark theme.</p>
              <div className="mt-6 flex gap-2">
                {(["light", "dark"] as Theme[]).map((value) => (
                  <Button
                    key={value}
                    variant={theme === value ? "primary" : "secondary"}
                    onClick={() => setTheme(value)}
                  >
                    {value === "light" ? "Light" : "Dark"}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {tab === "research" && (
            <form onSubmit={saveResearchProfile}>
              <h2 className="text-lg font-semibold text-foreground">Research profile</h2>
              <p className="mt-1 text-sm text-muted">Power discovery and collaboration matching.</p>
              {error && <div className="mt-4"><ErrorState description={error} /></div>}
              {loading && !profile ? (
                <div className="mt-6"><SkeletonText lines={6} /></div>
              ) : (
                <div className="mt-6 grid gap-3">
                  <textarea
                    value={form.bio}
                    onChange={(e) => setForm({ ...form, bio: e.target.value })}
                    className="min-h-24 rounded-lg border border-line bg-card px-3 py-2 text-sm"
                    placeholder="Bio"
                  />
                  <Input value={form.institution} onChange={(e) => setForm({ ...form, institution: e.target.value })} placeholder="Institution" />
                  <Input value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} placeholder="Department" />
                  <Input value={form.skills} onChange={(e) => setForm({ ...form, skills: e.target.value })} placeholder="Skills (comma-separated)" />
                  <Input value={form.interests} onChange={(e) => setForm({ ...form, interests: e.target.value })} placeholder="Research interests" />
                  <Input value={form.github_url} onChange={(e) => setForm({ ...form, github_url: e.target.value })} placeholder="GitHub URL" />
                  <Input value={form.linkedin_url} onChange={(e) => setForm({ ...form, linkedin_url: e.target.value })} placeholder="LinkedIn URL" />
                  <Input value={form.website_url} onChange={(e) => setForm({ ...form, website_url: e.target.value })} placeholder="Website URL" />
                  <Button type="submit" variant="primary" disabled={loading}>
                    {saved ? "Saved" : "Save profile"}
                  </Button>
                </div>
              )}
            </form>
          )}

          {tab === "privacy" && (
            <div>
              <h2 className="text-lg font-semibold text-foreground">Privacy</h2>
              <p className="mt-1 text-sm text-muted">Control profile visibility and data sharing.</p>
              <select
                value={form.visibility}
                onChange={(e) => setForm({ ...form, visibility: e.target.value })}
                className="mt-6 h-10 rounded-lg border border-line bg-card px-3 text-sm"
              >
                <option value="public">Public profile</option>
                <option value="workspace">Workspace only</option>
                <option value="private">Private</option>
              </select>
            </div>
          )}

          {tab === "accounts" && (
            <div>
              <h2 className="text-lg font-semibold text-foreground">Connected accounts</h2>
              <p className="mt-1 text-sm text-muted">Google Drive sync and external integrations (coming soon).</p>
              <div className="mt-6 space-y-3">
                <div className="flex items-center justify-between rounded-xl border border-line bg-card p-4">
                  <div className="flex items-center gap-3">
                    <Globe className="h-5 w-5 text-muted" />
                    <div>
                      <p className="text-sm font-medium text-foreground">Google Drive</p>
                      <p className="text-xs text-muted">Sync documents from Drive</p>
                    </div>
                  </div>
                  <Button variant="secondary" disabled>Connect</Button>
                </div>
                <div className="flex items-center justify-between rounded-xl border border-line bg-card p-4">
                  <div className="flex items-center gap-3">
                    <Github className="h-5 w-5 text-muted" />
                    <div>
                      <p className="text-sm font-medium text-foreground">GitHub</p>
                      <p className="text-xs text-muted">Link repositories to research profile</p>
                    </div>
                  </div>
                  <Button variant="secondary" disabled>Connect</Button>
                </div>
                <div className="flex items-center justify-between rounded-xl border border-line bg-card p-4">
                  <div className="flex items-center gap-3">
                    <Linkedin className="h-5 w-5 text-muted" />
                    <div>
                      <p className="text-sm font-medium text-foreground">LinkedIn</p>
                      <p className="text-xs text-muted">Import professional details</p>
                    </div>
                  </div>
                  <Button variant="secondary" disabled>Connect</Button>
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
