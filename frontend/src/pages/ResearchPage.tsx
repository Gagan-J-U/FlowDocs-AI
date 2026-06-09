import { Github, Globe, Linkedin, Search, UserRound } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Avatar } from "../components/ui/avatar";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { EmptyState, ErrorState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { Skeleton, SkeletonText } from "../components/ui/skeleton";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { ResearchProfile } from "../types";

export function ResearchDirectoryPage() {
  const { token } = useAppStore();
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<ResearchProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function search(event?: FormEvent) {
    event?.preventDefault();
    if (!token || !query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.discoverResearchers(token, query.trim());
      setResults(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Discovery failed");
    } finally {
      setLoading(false);
    }
  }

  async function messageResearcher(profile: ResearchProfile) {
    if (!token || !profile.user_id) return;
    try {
      const conversation = await api.createDmConversation(token, profile.user_id);
      navigate("/messages");
      setTimeout(() => {
        // Let MessagesPage pick up the new thread on navigation.
        void api.dmConversations(token);
      }, 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to start conversation");
    }
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Research directory</h1>
            <p className="mt-1 text-sm text-muted">Discover collaborators and message researchers directly.</p>
          </div>
          <Link to="/research/discover">
            <Button variant="primary">Discover researchers</Button>
          </Link>
        </div>

        <form onSubmit={search} className="mt-6 flex gap-2">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Semantic search researchers..." className="pl-9" />
          </div>
          <Button type="submit" variant="primary" disabled={loading}>Search</Button>
        </form>

        {error && <div className="mt-4"><ErrorState description={error} onRetry={() => void search()} /></div>}
        {loading && (
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <Skeleton className="h-40" />
            <Skeleton className="h-40" />
          </div>
        )}

        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {results.map((profile) => (
            <ResearchCard key={profile.user_id} profile={profile} onMessage={messageResearcher} />
          ))}
        </div>

        {!loading && !results.length && (
          <EmptyState
            icon={UserRound}
            title="Search the research directory"
            description="Find researchers by skills, interests, or institution."
          />
        )}
      </div>
    </div>
  );
}

export function DiscoverResearchersPage() {
  const { token } = useAppStore();
  const navigate = useNavigate();
  const [query, setQuery] = useState("machine learning retrieval augmented generation");
  const [results, setResults] = useState<ResearchProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function messageResearcher(profile: ResearchProfile) {
    if (!token || !profile.user_id) return;
    try {
      await api.createDmConversation(token, profile.user_id);
      navigate("/messages");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to start conversation");
    }
  }

  useEffect(() => {
    if (!token) return;
    void search();
  }, [token]);

  async function search(event?: FormEvent) {
    event?.preventDefault();
    if (!token || !query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.discoverResearchers(token, query.trim(), 12);
      setResults(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Discovery failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-2xl font-semibold text-foreground">Discover researchers</h1>
        <p className="mt-1 text-sm text-muted">Semantic matching for collaborators and similar profiles.</p>

        <form onSubmit={search} className="mt-6 flex gap-2">
          <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Describe your research interests..." />
          <Button type="submit" variant="primary" disabled={loading}>Discover</Button>
        </form>

        {error && <div className="mt-4"><ErrorState description={error} onRetry={() => void search()} /></div>}

        <div className="mt-8">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Suggested collaborators</h2>
          {loading ? (
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <Skeleton className="h-44" />
              <Skeleton className="h-44" />
            </div>
          ) : (
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {results.map((profile) => (
                <ResearchCard key={profile.user_id} profile={profile} showScore onMessage={messageResearcher} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function ResearchProfilePage() {
  const { userId } = useParams();
  const [profile, setProfile] = useState<ResearchProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;
    setLoading(true);
    void api.researchProfileByUser(userId)
      .then(setProfile)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load profile"))
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) {
    return (
      <div className="p-6">
        <Skeleton className="h-32 w-full max-w-3xl" />
        <div className="mt-4 max-w-3xl"><SkeletonText lines={5} /></div>
      </div>
    );
  }

  if (error || !profile) {
    return <ErrorState description={error ?? "Profile not found"} />;
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-3xl rounded-2xl border border-line bg-panel p-6">
        <div className="flex items-start gap-4">
          <Avatar name={profile.username ?? profile.user_id} />
          <div>
            <h1 className="text-2xl font-semibold text-foreground">{profile.username ?? "Researcher"}</h1>
            <p className="text-sm text-muted">
              {[profile.institution, profile.department].filter(Boolean).join(" · ") || "Independent researcher"}
            </p>
          </div>
        </div>

        {profile.bio && <p className="mt-6 text-sm leading-7 text-foreground">{profile.bio}</p>}

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <ProfileBlock title="Skills" content={profile.skills} />
          <ProfileBlock title="Interests" content={profile.interests} />
        </div>

        <div className="mt-6 flex flex-wrap gap-2">
          {profile.github_url && (
            <a href={profile.github_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 rounded-lg border border-line px-3 py-2 text-sm text-foreground hover:bg-subtle/40">
              <Github className="h-4 w-4" /> GitHub
            </a>
          )}
          {profile.linkedin_url && (
            <a href={profile.linkedin_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 rounded-lg border border-line px-3 py-2 text-sm text-foreground hover:bg-subtle/40">
              <Linkedin className="h-4 w-4" /> LinkedIn
            </a>
          )}
          {profile.website_url && (
            <a href={profile.website_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 rounded-lg border border-line px-3 py-2 text-sm text-foreground hover:bg-subtle/40">
              <Globe className="h-4 w-4" /> Website
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function ResearchCard({
  profile,
  showScore,
  onMessage,
}: {
  profile: ResearchProfile;
  showScore?: boolean;
  onMessage?: (profile: ResearchProfile) => void;
}) {
  const name = profile.username ?? `Researcher ${profile.user_id.slice(0, 6)}`;
  return (
    <div className="rounded-2xl border border-line bg-panel p-4 transition hover:border-brand/25 hover:shadow-soft">
      <div className="flex items-start gap-3">
        <Avatar name={name} />
        <div className="min-w-0 flex-1">
          <h3 className="truncate text-sm font-semibold text-foreground">{name}</h3>
          <p className="truncate text-xs text-muted">{profile.institution ?? "—"}</p>
        </div>
        {showScore && profile.similarity_score !== undefined && (
          <Badge variant="mint">{Math.round(profile.similarity_score * 100)}% match</Badge>
        )}
      </div>
      <p className="mt-3 line-clamp-3 text-xs leading-5 text-muted">{profile.bio ?? profile.interests ?? "No bio yet."}</p>
      {profile.skills && (
        <div className="mt-3 flex flex-wrap gap-1">
          {profile.skills.split(",").slice(0, 3).map((skill) => (
            <Badge key={skill} variant="outline">{skill.trim()}</Badge>
          ))}
        </div>
      )}
      <div className="mt-4 flex items-center gap-2">
        <Link to={`/research/profile/${profile.user_id}`} className="text-sm text-brand hover:underline">
          View profile
        </Link>
        {onMessage && (
          <Button type="button" size="sm" onClick={() => onMessage(profile)}>
            Message
          </Button>
        )}
      </div>
    </div>
  );
}

function ProfileBlock({ title, content }: { title: string; content?: string | null }) {
  if (!content) return null;
  return (
    <div className="rounded-xl border border-line bg-card p-4">
      <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-foreground">{content}</p>
    </div>
  );
}
