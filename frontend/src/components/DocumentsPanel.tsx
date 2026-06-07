import { ChangeEvent, useState } from "react";
import { AlertCircle, FileText, UploadCloud } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";

export function DocumentsPanel() {
  const { token, selectedSubjectId, documents, setDocuments } = useAppStore();
  const [progress, setProgress] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function upload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !selectedSubjectId) return;

    setError(null);
    setProgress(1);
    try {
      const document = await api.uploadDocument(token, selectedSubjectId, file, setProgress);
      setDocuments([document, ...documents]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setProgress(null);
      event.target.value = "";
    }
  }

  return (
    <section className="glass rounded-xl p-4">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-foreground dark:text-white">Documents</h2>
          <p className="text-xs text-muted">{documents.length} sources in this subject</p>
        </div>
        <label
          className={`inline-flex h-9 w-9 cursor-pointer items-center justify-center rounded-lg border transition ${
            selectedSubjectId
              ? "border-brand/40 bg-brand/90 text-white shadow-glow hover:bg-brand dark:text-ink"
              : "pointer-events-none border-line bg-card text-muted opacity-45"
          }`}
          aria-label="Upload PDF"
          title="Upload PDF"
        >
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={upload}
            disabled={!selectedSubjectId}
          />
          <UploadCloud className="h-4 w-4" />
        </label>
      </div>
      {progress !== null && (
        <div className="mb-3 h-1.5 overflow-hidden rounded-full bg-subtle dark:bg-white/10">
          <div className="h-full rounded-full bg-brand transition-all" style={{ width: `${progress}%` }} />
        </div>
      )}
      {error && (
        <div className="mb-3 flex gap-2 rounded-lg border border-red-400/25 bg-red-500/10 px-3 py-2 text-xs leading-5 text-red-700 dark:text-red-100">
          <AlertCircle className="mt-0.5 h-3.5 w-3.5 flex-none" />
          <span>{error}</span>
        </div>
      )}
      <div className="grid max-h-44 gap-2 overflow-y-auto">
        {documents.map((document) => (
          <div key={document.id} className="flex gap-3 rounded-lg border border-line/70 bg-card/75 p-3 dark:border-white/10 dark:bg-white/[0.04]">
            <FileText className="mt-0.5 h-4 w-4 flex-none text-brand" />
            <div className="min-w-0">
              <div className="truncate text-sm text-foreground dark:text-slate-100">{document.filename}</div>
              <div className="text-xs text-muted">
                {document.file_size ? `${Math.round(document.file_size / 1024)} KB` : "Processing"}
              </div>
            </div>
          </div>
        ))}
        {!documents.length && (
          <div className="rounded-lg border border-dashed border-line/80 p-4 text-sm text-muted dark:border-white/10">
            Upload PDFs to make this subject searchable.
          </div>
        )}
      </div>
    </section>
  );
}
