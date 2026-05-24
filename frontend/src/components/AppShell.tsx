import { useEffect, useState } from "react";
import { PanelLeft } from "lucide-react";
import { api } from "../lib/api";
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
  } = useAppStore();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!token) return;

    async function loadBase() {
      const [workspaces, subjects] = await Promise.all([
        api.workspaces(token!),
        api.subjects(token!),
      ]);
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
    }

    void loadBase();
  }, [token]);

  useEffect(() => {
    if (!token || !selectedWorkspaceId) {
      setConversations([]);
      return;
    }

    void api.conversations(token, selectedWorkspaceId).then(setConversations);
  }, [token, selectedWorkspaceId, setConversations]);

  useEffect(() => {
    if (!token || !selectedSubjectId) {
      setDocuments([]);
      return;
    }

    void api.documents(token, selectedSubjectId).then(setDocuments);
  }, [token, selectedSubjectId, setDocuments]);

  return (
    <div className="h-screen overflow-hidden p-2 md:p-4">
      <div className="glass grid h-full overflow-hidden rounded-2xl shadow-panel lg:grid-cols-[320px_minmax(0,1fr)] xl:grid-cols-[320px_minmax(0,1fr)_360px]">
        <div className="hidden min-h-0 lg:block">
          <Sidebar />
        </div>
        <div className="fixed left-3 top-3 z-40 lg:hidden">
          <Button variant="secondary" size="icon" onClick={() => setSidebarOpen(true)} aria-label="Open sidebar">
            <PanelLeft className="h-4 w-4" />
          </Button>
        </div>
        {sidebarOpen && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm lg:hidden" onClick={() => setSidebarOpen(false)}>
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
