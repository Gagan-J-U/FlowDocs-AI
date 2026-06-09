import { FormEvent, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, FileText, MessageSquare, Plus } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import { EmptyState } from "../components/ui/empty-state";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Skeleton } from "../components/ui/skeleton";

export function SubjectsPage() {
  const {
    token,
    subjects,
    documents,
    conversations,
    selectedWorkspaceId,
    selectedSubjectId,
    setSubjects,
    setSelectedSubjectId,
  } = useAppStore();
  const [subjectName, setSubjectName] = useState("");
  const [loading, setLoading] = useState(false);

  const visibleSubjects = useMemo(
    () => subjects.filter((s) => s.workspace_id === selectedWorkspaceId),
    [subjects, selectedWorkspaceId],
  );

  async function createSubject(event: FormEvent) {
    event.preventDefault();
    if (!token || !selectedWorkspaceId || !subjectName.trim()) return;
    setLoading(true);
    try {
      const subject = await api.createSubject(token, subjectName.trim(), selectedWorkspaceId);
      setSubjects([subject, ...subjects]);
      setSelectedSubjectId(subject.id);
      setSubjectName("");
    } finally {
      setLoading(false);
    }
  }

  if (!selectedWorkspaceId) {
    return (
      <EmptyState
        icon={BookOpen}
        title="Select a workspace"
        description="Choose or create a workspace to manage subjects."
      />
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Subjects</h1>
            <p className="mt-1 text-sm text-muted">Organize research topics within your workspace.</p>
          </div>
          <form onSubmit={createSubject} className="flex gap-2">
            <Input value={subjectName} onChange={(e) => setSubjectName(e.target.value)} placeholder="New subject" />
            <Button type="submit" variant="primary" disabled={loading}>
              <Plus className="h-4 w-4" />
              Create
            </Button>
          </form>
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {visibleSubjects.map((subject, index) => {
            const docCount = documents.filter((d) => d.subject_id === subject.id).length;
            const convCount = conversations.length;
            return (
              <motion.button
                key={subject.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.04 }}
                onClick={() => setSelectedSubjectId(subject.id)}
                className={`rounded-2xl border p-5 text-left transition hover:-translate-y-0.5 ${
                  selectedSubjectId === subject.id
                    ? "border-brand/30 bg-brand/5 shadow-soft"
                    : "border-line bg-panel hover:border-brand/20"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand/10 text-brand">
                    <BookOpen className="h-5 w-5" />
                  </div>
                  {selectedSubjectId === subject.id && (
                    <span className="rounded-full bg-brand/10 px-2 py-0.5 text-[10px] font-medium text-brand">Active</span>
                  )}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-foreground">{subject.name}</h3>
                <div className="mt-4 grid grid-cols-3 gap-2">
                  <Stat label="Documents" value={docCount} icon={FileText} />
                  <Stat label="Conversations" value={convCount} icon={MessageSquare} />
                  <Stat label="Figures" value="—" icon={BookOpen} />
                </div>
              </motion.button>
            );
          })}
        </div>

        {!visibleSubjects.length && !loading && (
          <EmptyState
            icon={BookOpen}
            title="No subjects yet"
            description="Create your first subject to start uploading documents and chatting."
          />
        )}
        {loading && <Skeleton className="mt-4 h-32" />}
      </div>
    </div>
  );
}

function Stat({ label, value, icon: Icon }: { label: string; value: string | number; icon: typeof FileText }) {
  return (
    <div className="rounded-lg bg-subtle/40 px-2 py-2">
      <div className="flex items-center gap-1 text-[10px] uppercase tracking-wide text-muted">
        <Icon className="h-3 w-3" />
        {label}
      </div>
      <p className="mt-1 text-sm font-semibold text-foreground">{value}</p>
    </div>
  );
}
