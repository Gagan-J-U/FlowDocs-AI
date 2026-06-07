import { ExternalLink } from "lucide-react";
import type { Citation } from "../types";
import { useAppStore } from "../store/app-store";
import { ComparisonPanel } from "./ComparisonPanel";
import { DocumentsPanel } from "./DocumentsPanel";

function citationTitle(citation: Citation) {
  return citation.section_title ?? citation.section ?? citation.filename ?? citation.document ?? "Retrieved source";
}

function citationPages(citation: Citation) {
  if (citation.start_page && citation.end_page) return `${citation.start_page}-${citation.end_page}`;
  if (Array.isArray(citation.pages)) return citation.pages.join(", ");
  return citation.pages ?? citation.page ?? "Unknown";
}

function citationSnippet(citation: Citation) {
  return citation.snippet ?? citation.text ?? "No snippet preview returned for this citation.";
}

export function CitationPanel() {
  const { selectedCitation, messages, setSelectedCitation } = useAppStore();
  const citations = messages.flatMap((message) => message.citations ?? []);

  return (
    <aside className="hidden min-h-0 flex-col gap-4 border-l border-line/70 bg-panel/65 p-4 xl:flex dark:border-white/10 dark:bg-black/20">
      <DocumentsPanel />
      <ComparisonPanel />
      <section className="glass min-h-0 flex-1 rounded-xl p-4">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-semibold text-foreground dark:text-white">Citations</h2>
            <p className="text-xs text-muted">{citations.length} retrieved references</p>
          </div>
          <ExternalLink className="h-4 w-4 text-muted" />
        </div>
        <div className="grid max-h-[calc(100vh-39rem)] gap-2 overflow-y-auto pr-1">
          {citations.map((citation, index) => (
            <button
              key={`${citationTitle(citation)}-${index}`}
              onClick={() => setSelectedCitation(citation)}
              className={`rounded-xl border p-3 text-left transition ${
                selectedCitation === citation
                  ? "border-brand/40 bg-brand/10"
                  : "border-line/70 bg-card/75 hover:bg-subtle/40 dark:border-white/10 dark:bg-white/[0.04] dark:hover:bg-white/[0.07]"
              }`}
            >
              <div className="text-xs font-medium text-brand">[{index + 1}] Pages {citationPages(citation)}</div>
              <div className="mt-1 line-clamp-2 text-sm text-foreground dark:text-slate-100">{citationTitle(citation)}</div>
              <p className="mt-2 line-clamp-3 text-xs leading-5 text-muted">{citationSnippet(citation)}</p>
            </button>
          ))}
          {!citations.length && (
            <div className="rounded-lg border border-dashed border-line/80 p-4 text-sm text-muted dark:border-white/10">
              Citations will appear here during completed AI responses.
            </div>
          )}
        </div>
      </section>
    </aside>
  );
}
