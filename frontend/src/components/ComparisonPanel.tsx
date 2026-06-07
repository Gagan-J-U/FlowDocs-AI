import { FormEvent, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import { GitCompareArrows, Loader2 } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { Citation, ComparisonResult } from "../types";
import { Button } from "./ui/button";

function resultText(result: ComparisonResult | null) {
  if (!result) return "";
  return String(result.answer ?? result.result ?? result.comparison ?? "");
}

function allSources(result: ComparisonResult | null): Citation[] {
  if (!result) return [];
  return [
    ...(result.document_a_sources ?? []),
    ...(result.document_b_sources ?? []),
    ...(result.sources ?? []),
  ];
}

export function ComparisonPanel() {
  const {
    token,
    selectedWorkspaceId,
    selectedSubjectId,
    documents,
    provider,
    setSelectedCitation,
  } = useAppStore();
  const [documentAId, setDocumentAId] = useState("");
  const [documentBId, setDocumentBId] = useState("");
  const [query, setQuery] = useState("Compare the key claims, gaps, and contradictions.");
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const selectableDocuments = useMemo(() => documents.slice(0, 20), [documents]);
  const sources = allSources(result);
  const canCompare = Boolean(
    token &&
    selectedWorkspaceId &&
    selectedSubjectId &&
    documentAId &&
    documentBId &&
    documentAId !== documentBId &&
    query.trim(),
  );

  async function compare(event: FormEvent) {
    event.preventDefault();
    if (!canCompare || !token || !selectedWorkspaceId || !selectedSubjectId) return;

    setLoading(true);
    setError(null);
    try {
      const next = await api.compareDocuments(token, {
        workspaceId: selectedWorkspaceId,
        subjectId: selectedSubjectId,
        documentAId,
        documentBId,
        query: query.trim(),
        provider,
      });
      setResult(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Comparison failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="glass rounded-xl p-4">
      <div className="mb-3 flex items-center gap-2">
        <GitCompareArrows className="h-4 w-4 text-mint" />
        <div>
          <h2 className="text-sm font-semibold text-foreground dark:text-white">Compare</h2>
          <p className="text-xs text-muted">Run the new document comparison route</p>
        </div>
      </div>

      <form onSubmit={compare} className="grid gap-2">
        <select
          value={documentAId}
          onChange={(event) => setDocumentAId(event.target.value)}
          className="h-9 rounded-lg border border-line/80 bg-card/80 px-3 text-sm text-foreground outline-none focus:border-brand/60 dark:border-white/10 dark:bg-white/[0.06] dark:text-slate-100"
        >
          <option value="">First document</option>
          {selectableDocuments.map((document) => (
            <option key={document.id} value={document.id}>{document.filename}</option>
          ))}
        </select>
        <select
          value={documentBId}
          onChange={(event) => setDocumentBId(event.target.value)}
          className="h-9 rounded-lg border border-line/80 bg-card/80 px-3 text-sm text-foreground outline-none focus:border-brand/60 dark:border-white/10 dark:bg-white/[0.06] dark:text-slate-100"
        >
          <option value="">Second document</option>
          {selectableDocuments.map((document) => (
            <option key={document.id} value={document.id}>{document.filename}</option>
          ))}
        </select>
        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="min-h-20 resize-none rounded-lg border border-line/80 bg-card/80 px-3 py-2 text-sm leading-6 text-foreground outline-none placeholder:text-muted focus:border-brand/60 dark:border-white/10 dark:bg-white/[0.06] dark:text-slate-100"
          placeholder="What should FlowDocs compare?"
        />
        <Button type="submit" variant="primary" disabled={!canCompare || loading}>
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <GitCompareArrows className="h-4 w-4" />}
          Compare
        </Button>
      </form>

      {error && (
        <div className="mt-3 rounded-lg border border-red-400/25 bg-red-500/10 px-3 py-2 text-xs text-red-700 dark:text-red-100">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-3 max-h-72 overflow-y-auto rounded-lg border border-line/70 bg-card/70 p-3 dark:border-white/10 dark:bg-white/[0.04]">
          <div className="markdown-stream prose max-w-none text-sm leading-6 text-foreground prose-p:text-foreground dark:prose-invert dark:text-slate-100">
            <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
              {resultText(result) || "Comparison completed."}
            </ReactMarkdown>
          </div>
          {sources.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {sources.slice(0, 8).map((source, index) => (
                <button
                  key={`${source.document_id ?? source.filename ?? "source"}-${index}`}
                  type="button"
                  onClick={() => setSelectedCitation(source)}
                  className="rounded-full border border-mint/30 bg-mint/10 px-2.5 py-1 text-xs text-mint transition hover:bg-mint/20"
                >
                  Source {index + 1}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
