import { FormEvent, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import { GitCompareArrows, Loader2 } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { Citation, ComparisonResult, FigureReference } from "../types";
import { Button } from "./ui/button";
import { ErrorState } from "./ui/empty-state";
import { FigureModal, FigureThumbnail } from "./figures/FigurePreview";

function resultText(result: ComparisonResult | null) {
  if (!result) return "";
  return String(result.answer ?? result.result ?? result.comparison ?? "").trim();
}

function allSources(result: ComparisonResult | null): Citation[] {
  if (!result) return [];
  return [
    ...(result.document_a_sources ?? []),
    ...(result.document_b_sources ?? []),
    ...(result.sources ?? []),
  ];
}

interface ComparisonPanelProps {
  compact?: boolean;
}

export function ComparisonPanel({ compact = false }: ComparisonPanelProps) {
  const {
    token,
    selectedWorkspaceId,
    selectedSubjectId,
    documents,
    provider,
    comparisonResult,
    comparisonLoading,
    comparisonError,
    setComparisonResult,
    setComparisonLoading,
    setComparisonError,
    setSelectedCitation,
  } = useAppStore();

  const [documentAId, setDocumentAId] = useState("");
  const [documentBId, setDocumentBId] = useState("");
  const [query, setQuery] = useState("Compare the key claims, gaps, and contradictions.");
  const [expandedFigure, setExpandedFigure] = useState<FigureReference | null>(null);

  const selectableDocuments = useMemo(() => documents, [documents]);
  const sources = allSources(comparisonResult);
  const answer = resultText(comparisonResult);
  const figures = (comparisonResult?.figures ?? []) as FigureReference[];

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

    setComparisonLoading(true);
    setComparisonError(null);
    try {
      const next = await api.compareDocuments(token, {
        workspaceId: selectedWorkspaceId,
        subjectId: selectedSubjectId,
        documentAId,
        documentBId,
        query: query.trim(),
        provider,
      });
      setComparisonResult(next);
      if (!resultText(next)) {
        setComparisonError("Comparison completed but returned no content. Check document indexing and LLM provider.");
      }
    } catch (err) {
      setComparisonError(err instanceof Error ? err.message : "Comparison failed");
      setComparisonResult(null);
    } finally {
      setComparisonLoading(false);
    }
  }

  return (
    <section className={compact ? "rounded-xl border border-line bg-panel p-4" : "space-y-4"}>
      {!compact && (
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Document comparison</h1>
          <p className="mt-1 text-sm text-muted">
            Compare two documents side by side with grounded citations and figure context.
          </p>
        </div>
      )}

      <div className={compact ? "" : "rounded-xl border border-line bg-panel p-5"}>
        {compact && (
          <div className="mb-3 flex items-center gap-2">
            <GitCompareArrows className="h-4 w-4 text-mint" />
            <h2 className="text-sm font-semibold text-foreground">Compare documents</h2>
          </div>
        )}

        <form onSubmit={compare} className="grid gap-3 md:grid-cols-2">
          <select
            value={documentAId}
            onChange={(event) => setDocumentAId(event.target.value)}
            className="h-10 rounded-lg border border-line bg-card px-3 text-sm text-foreground outline-none focus:border-brand/50"
          >
            <option value="">First document</option>
            {selectableDocuments.map((document) => (
              <option key={document.id} value={document.id}>{document.filename}</option>
            ))}
          </select>
          <select
            value={documentBId}
            onChange={(event) => setDocumentBId(event.target.value)}
            className="h-10 rounded-lg border border-line bg-card px-3 text-sm text-foreground outline-none focus:border-brand/50"
          >
            <option value="">Second document</option>
            {selectableDocuments.map((document) => (
              <option key={document.id} value={document.id}>{document.filename}</option>
            ))}
          </select>
          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="min-h-24 resize-none rounded-lg border border-line bg-card px-3 py-2 text-sm leading-6 text-foreground outline-none focus:border-brand/50 md:col-span-2"
            placeholder="What should FlowDocs compare?"
          />
          <Button type="submit" variant="primary" disabled={!canCompare || comparisonLoading} className="md:col-span-2">
            {comparisonLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <GitCompareArrows className="h-4 w-4" />}
            Run comparison
          </Button>
        </form>

        {comparisonError && (
          <div className="mt-4">
            <ErrorState description={comparisonError} />
          </div>
        )}

        {comparisonResult && (
          <div className="mt-5 space-y-4">
            {(comparisonResult.document_a_summary || comparisonResult.document_b_summary) && (
              <div className="grid gap-3 md:grid-cols-2">
                {comparisonResult.document_a_summary && (
                  <div className="rounded-lg border border-line bg-subtle/20 p-3">
                    <p className="text-xs font-medium uppercase tracking-wide text-muted">Document A</p>
                    <p className="mt-2 text-sm leading-6 text-foreground">{String(comparisonResult.document_a_summary)}</p>
                  </div>
                )}
                {comparisonResult.document_b_summary && (
                  <div className="rounded-lg border border-line bg-subtle/20 p-3">
                    <p className="text-xs font-medium uppercase tracking-wide text-muted">Document B</p>
                    <p className="mt-2 text-sm leading-6 text-foreground">{String(comparisonResult.document_b_summary)}</p>
                  </div>
                )}
              </div>
            )}

            {answer && (
              <div className="rounded-xl border border-line bg-card p-4">
                <p className="mb-3 text-xs font-medium uppercase tracking-wide text-brand">Analysis</p>
                <div className="markdown-stream prose max-w-none text-sm leading-7 text-foreground dark:prose-invert">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
                    {answer}
                  </ReactMarkdown>
                </div>
              </div>
            )}

            {sources.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted">Sources</p>
                <div className="flex flex-wrap gap-2">
                  {sources.map((source, index) => (
                    <button
                      key={`${source.document_id ?? source.filename ?? "source"}-${index}`}
                      type="button"
                      onClick={() => setSelectedCitation(source)}
                      className="rounded-full border border-mint/30 bg-mint/10 px-3 py-1 text-xs text-mint transition hover:bg-mint/20"
                    >
                      Source {index + 1}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {figures.length > 0 && (
              <div>
                <p className="mb-3 text-xs font-medium uppercase tracking-wide text-muted">Related figures</p>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {figures.map((figure, index) => (
                    <FigureThumbnail
                      key={`${figure.figure_id ?? index}`}
                      figure={figure}
                      index={index}
                      onExpand={() => setExpandedFigure(figure)}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <FigureModal figure={expandedFigure} onClose={() => setExpandedFigure(null)} />
    </section>
  );
}
