import { FileText, Grid3X3, List, Search, Upload } from "lucide-react";
import { useMemo, useState } from "react";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { EmptyState, ErrorState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { Skeleton } from "../components/ui/skeleton";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import { useUiStore } from "../store/ui-store";

export function DocumentsPage() {
  const { token, documents, selectedSubjectId, setDocuments } = useAppStore();
  const { documentViewMode, setDocumentViewMode } = useUiStore();
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<"date" | "name">("date");
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();
    let items = [...documents];
    if (query) {
      items = items.filter((doc) => doc.filename.toLowerCase().includes(query));
    }
    items.sort((a, b) => {
      if (sort === "name") return a.filename.localeCompare(b.filename);
      return new Date(b.uploaded_at).getTime() - new Date(a.uploaded_at).getTime();
    });
    return items;
  }, [documents, search, sort]);

  async function upload(file: File) {
    if (!token || !selectedSubjectId) return;
    setUploading(true);
    setError(null);
    setProgress(0);
    try {
      const record = await api.uploadDocument(token, selectedSubjectId, file, setProgress);
      setDocuments([record, ...documents]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  if (!selectedSubjectId) {
    return (
      <EmptyState
        icon={FileText}
        title="Select a subject"
        description="Choose a subject to view and upload documents."
      />
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Document library</h1>
            <p className="mt-1 text-sm text-muted">{filtered.length} documents in this subject</p>
          </div>
          <label className="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-brand/40 bg-brand px-4 py-2 text-sm text-white transition hover:bg-brand/90">
            <input
              type="file"
              accept="application/pdf"
              className="hidden"
              disabled={uploading}
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (file) void upload(file);
              }}
            />
            <Upload className="h-4 w-4" />
            Upload PDF
          </label>
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <div className="relative min-w-[220px] flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search documents..." className="pl-9" />
          </div>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as "date" | "name")}
            className="h-10 rounded-lg border border-line bg-card px-3 text-sm"
          >
            <option value="date">Sort by date</option>
            <option value="name">Sort by name</option>
          </select>
          <div className="flex rounded-lg border border-line p-1">
            <Button
              variant={documentViewMode === "grid" ? "primary" : "ghost"}
              size="icon"
              onClick={() => setDocumentViewMode("grid")}
            >
              <Grid3X3 className="h-4 w-4" />
            </Button>
            <Button
              variant={documentViewMode === "list" ? "primary" : "ghost"}
              size="icon"
              onClick={() => setDocumentViewMode("list")}
            >
              <List className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {uploading && (
          <div className="mt-4">
            <Skeleton className="h-2" />
            <p className="mt-1 text-xs text-muted">Uploading… {progress}%</p>
          </div>
        )}
        {error && <div className="mt-4"><ErrorState description={error} onRetry={() => setError(null)} /></div>}

        {documentViewMode === "grid" ? (
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((doc) => (
              <article key={doc.id} className="rounded-xl border border-line bg-panel p-4 transition hover:border-brand/20">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand/10 text-brand">
                  <FileText className="h-5 w-5" />
                </div>
                <h3 className="mt-3 line-clamp-2 text-sm font-semibold text-foreground">{doc.filename}</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Badge variant="outline">{new Date(doc.uploaded_at).toLocaleString()}</Badge>
                  <Badge variant="mint">
                    {doc.processing_status
                      ? doc.processing_status.replace(/_/g, " ")
                      : "Pending"}
                  </Badge>
                </div>
                <p className="mt-2 text-xs text-muted">
                  {doc.file_size ? `${Math.round(doc.file_size / 1024)} KB` : "Unknown size"}
                </p>
              </article>
            ))}
          </div>
        ) : (
          <div className="mt-6 overflow-hidden rounded-xl border border-line">
            <table className="w-full text-left text-sm">
              <thead className="bg-subtle/40 text-xs uppercase tracking-wide text-muted">
                <tr>
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Uploaded</th>
                  <th className="px-4 py-3">Size</th>
                  <th className="px-4 py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((doc) => (
                  <tr key={doc.id} className="border-t border-line">
                    <td className="px-4 py-3 font-medium text-foreground">{doc.filename}</td>
                    <td className="px-4 py-3 text-muted">{new Date(doc.uploaded_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-muted">{doc.file_size ? `${Math.round(doc.file_size / 1024)} KB` : "—"}</td>
                    <td className="px-4 py-3"><Badge variant="mint">
                      {doc.processing_status
                        ? doc.processing_status.replace(/_/g, " ")
                        : "Pending"}
                    </Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!filtered.length && !uploading && (
          <EmptyState
            icon={FileText}
            title="No documents"
            description="Upload PDFs to build your research corpus."
          />
        )}
      </div>
    </div>
  );
}
