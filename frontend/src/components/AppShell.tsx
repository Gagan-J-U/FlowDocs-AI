import { useEffect, useState } from "react";
import { Loader2, PanelLeft } from "lucide-react";
import { BrowserRouter, useLocation } from "react-router-dom";
import { api, isAuthError } from "../lib/api";
import type { User } from "../store/app-store";
import { useAppStore } from "../store/app-store";
import { useUiStore } from "../store/ui-store";
import { Button } from "./ui/button";
import { Sidebar } from "./layout/Sidebar";
import { CitationPanel } from "./CitationPanel";
import { AppRoutes } from "../routes/AppRoutes";

export function AppShell() {
  return (
    <BrowserRouter>
      <AppShellInner />
    </BrowserRouter>
  );
}

function AppShellInner() {
  const location = useLocation();
  const showCitationPanel = ["/chat", "/comparisons"].some((path) => location.pathname.startsWith(path));
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
    setUser,
    resetSession,
  } = useAppStore();
  const { sidebarOpen, setSidebarOpen } = useUiStore();
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;

    async function loadBase() {
      setCheckingSession(true);
      try {
        const [workspaces, subjects, me] = await Promise.all([
          api.workspaces(token!),
          api.subjects(token!),
          api.me(token!),
        ]);

        if (cancelled) return;

        const user: User = { id: me.id, username: me.username, email: me.email };
        setUser(user);
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
      <div className="grid h-screen place-items-center bg-ink text-foreground">
        <div className="flex items-center gap-3 rounded-xl border border-line bg-panel px-4 py-3 text-sm text-muted">
          <Loader2 className="h-4 w-4 animate-spin text-brand" />
          Loading workspace
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-ink text-foreground">
      <div className="hidden min-h-0 lg:flex">
        <Sidebar />
      </div>

      <div className="fixed left-3 top-3 z-40 lg:hidden">
        <Button variant="secondary" size="icon" onClick={() => setSidebarOpen(true)} aria-label="Open sidebar">
          <PanelLeft className="h-4 w-4" />
        </Button>
      </div>

      {sidebarOpen && (
        <div className="fixed inset-0 z-50 bg-ink/70 lg:hidden" onClick={() => setSidebarOpen(false)}>
          <div className="h-full w-[86vw] max-w-[280px]" onClick={(event) => event.stopPropagation()}>
            <Sidebar />
          </div>
        </div>
      )}

      <div className="flex min-h-0 min-w-0 flex-1">
        <main className="flex min-h-0 min-w-0 flex-1 flex-col">
          <AppRoutes />
        </main>
        {showCitationPanel && <CitationPanel />}
      </div>
    </div>
  );
}
