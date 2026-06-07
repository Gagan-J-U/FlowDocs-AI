import { useEffect, useState } from "react";
import { Loader2, PanelLeft } from "lucide-react";
import { api, isAuthError } from "../lib/api";
import { useAppStore } from "../store/app-store";
import { Button } from "./ui/button";
import { ChatPanel } from "./ChatPanel";
import { CitationPanel } from "./CitationPanel";
import { Sidebar } from "./Sidebar";

export function AppShell() {
  const {
    token,
    selectedWorkspaceId,
    selectedSubjectId,
    setWorkspaces,
    setSubjects,
    setDocuments,
    setConversations,
    setSelectedWorkspaceId,
    setSelectedSubjectId,
    resetSession,
  } = useAppStore();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;

    async function loadBase() {
      setCheckingSession(true);
      try {
        const [workspaces, subjects] = await Promise.all([
          api.workspaces(token!),
          api.subjects(token!),
        ]);

        if (cancelled) return;

        setWorkspaces(workspaces);
        setSubjects(subjects);

        if (!selectedWorkspaceId && workspaces[0]) {
          setSelectedWorkspaceId(workspaces[0].id);
        }

        const workspaceId = selectedWorkspaceId ?? workspaces[0]?.id;
        const subject = subjects.find((item) => item.workspace_id === workspaceId);
        if (!selectedSubjectId && subject) {
          setSelectedSubjectId(subject.id);
        }
      } catch (error) {
        if (!cancelled && isAuthError(error)) {
          resetSession();
        }
      } finally {
        if (!cancelled) {
          setCheckingSession(false);
        }
      }
    }

    void loadBase();
    return () => {
      cancelled = true;
    };
  }, [token, resetSession, selectedSubjectId, selectedWorkspaceId, setSelectedSubjectId, setSelectedWorkspaceId, setSubjects, setWorkspaces]);

  useEffect(() => {
    if (!token || !selectedWorkspaceId) {
      setConversations([]);
      return;
    }

    void api.conversations(token, selectedWorkspaceId)
      .then(setConversations)
      .catch((error) => {
        if (isAuthError(error)) resetSession();
      });
  }, [token, selectedWorkspaceId, setConversations, resetSession]);

  useEffect(() => {
    if (!token || !selectedSubjectId) {
      setDocuments([]);
      return;
    }

    void api.documents(token, selectedSubjectId)
      .then(setDocuments)
      .catch((error) => {
        if (isAuthError(error)) resetSession();
      });
  }, [token, selectedSubjectId, setDocuments, resetSession]);

  if (checkingSession) {
    return (
      <div className="grid h-screen place-items-center text-foreground">
        <div className="glass flex items-center gap-3 rounded-xl px-4 py-3 text-sm text-muted">
          <Loader2 className="h-4 w-4 animate-spin text-brand" />
          Checking session
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden p-2 text-foreground md:p-4">
      <div className="glass grid h-full overflow-hidden rounded-2xl shadow-panel lg:grid-cols-[300px_minmax(0,1fr)] xl:grid-cols-[300px_minmax(0,1fr)_380px]">
        <div className="hidden min-h-0 lg:block">
          <Sidebar />
        </div>
        <div className="fixed left-3 top-3 z-40 lg:hidden">
          <Button variant="secondary" size="icon" onClick={() => setSidebarOpen(true)} aria-label="Open sidebar">
            <PanelLeft className="h-4 w-4" />
          </Button>
        </div>
        {sidebarOpen && (
          <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm lg:hidden" onClick={() => setSidebarOpen(false)}>
            <div className="h-full w-[86vw] max-w-sm" onClick={(event) => event.stopPropagation()}>
              <Sidebar />
            </div>
          </div>
        )}
        <ChatPanel />
        <CitationPanel />
      </div>
    </div>
  );
}
