import { ChangeEvent, useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import { Button } from "./ui/button";

export function DocumentsPanel() {
  const { token, selectedSubjectId, documents, setDocuments } = useAppStore();
  const [progress, setProgress] = useState<number | null>(null);

  async function upload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !selectedSubjectId) return;

    setProgress(1);
    try {
      const document = await api.uploadDocument(token, selectedSubjectId, file, setProgress);
      setDocuments([document, ...documents]);
    } finally {
      setProgress(null);
      event.target.value = "";
    }
  }

  return (
    <section className="glass rounded-xl p-4">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-white">Documents</h2>
          <p className="text-xs text-slate-500">{documents.length} sources in this subject</p>
        </div>
        <label>
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={upload}
            disabled={!selectedSubjectId}
          />
          <Button size="icon" disabled={!selectedSubjectId} aria-label="Upload PDF">
            <UploadCloud className="h-4 w-4" />
          </Button>
        </label>
      </div>
      {progress !== null && (
        <div className="mb-3 h-1.5 overflow-hidden rounded-full bg-white/10">
          <div className="h-full rounded-full bg-brand transition-all" style={{ width: `${progress}%` }} />
        </div>
      )}
      <div className="grid max-h-44 gap-2 overflow-y-auto">
        {documents.map((document) => (
          <div key={document.id} className="flex gap-3 rounded-lg border border-white/10 bg-white/[0.04] p-3">
            <FileText className="mt-0.5 h-4 w-4 flex-none text-brand" />
            <div className="min-w-0">
              <div className="truncate text-sm text-slate-100">{document.filename}</div>
              <div className="text-xs text-slate-500">
                {document.file_size ? `${Math.round(document.file_size / 1024)} KB` : "Processing"}
              </div>
            </div>
          </div>
        ))}
        {!documents.length && (
          <div className="rounded-lg border border-dashed border-white/10 p-4 text-sm text-slate-500">
            Upload PDFs to make this subject searchable.
          </div>
        )}
      </div>
    </section>
  );
}
