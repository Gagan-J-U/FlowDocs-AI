import { FileText, Quote } from "lucide-react";
import { useAppStore } from "../store/app-store";
import { ComparisonPanel } from "./ComparisonPanel";

function titleFor(citation: NonNullable<ReturnType<typeof useAppStore.getState>["selectedCitation"]>) {
  if (!citation) return "Source";
  return citation.section_title ?? citation.section ?? citation.filename ?? "Source";
}

export function CitationPanel() {
  const selectedCitation = useAppStore((state) => state.selectedCitation);
  const setSelectedCitation = useAppStore((state) => state.setSelectedCitation);

  return (
    <aside className="hidden min-h-0 w-[340px] flex-col overflow-y-auto border-l border-line bg-panel xl:flex">
      <div className="border-b border-line p-4">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted">
          <Quote className="h-3.5 w-3.5" />
          Citations
        </div>
        {selectedCitation ? (
          <div className="mt-3 rounded-xl border border-line bg-card p-3">
            <div className="flex items-start justify-between gap-2">
              <h3 className="text-sm font-semibold text-foreground">{titleFor(selectedCitation)}</h3>
              <button
                type="button"
                className="text-xs text-muted hover:text-foreground"
                onClick={() => setSelectedCitation(null)}
              >
                Clear
              </button>
            </div>
            {(selectedCitation.page || selectedCitation.pages) && (
              <p className="mt-1 text-xs text-muted">
                Page {String(selectedCitation.page ?? selectedCitation.pages)}
              </p>
            )}
            <p className="mt-3 text-sm leading-6 text-foreground">
              {String(selectedCitation.snippet ?? selectedCitation.text ?? "No excerpt available.")}
            </p>
            {selectedCitation.filename && (
              <p className="mt-2 flex items-center gap-1 text-xs text-muted">
                <FileText className="h-3 w-3" />
                {selectedCitation.filename}
              </p>
            )}
          </div>
        ) : (
          <p className="mt-3 text-sm text-muted">Select a citation chip from chat or comparison results.</p>
        )}
      </div>

      <div className="p-4">
        <ComparisonPanel compact />
      </div>
    </aside>
  );
}
