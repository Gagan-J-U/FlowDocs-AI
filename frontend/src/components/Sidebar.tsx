import { FormEvent, useMemo, useState } from "react";
import { MessageSquare, Moon, Plus, Sun, Trash2, UsersRound } from "lucide-react";
import { api } from "../lib/api";
import { formatRelativeTime } from "../lib/utils";
import { useAppStore } from "../store/app-store";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

export function Sidebar() {
  const {
    token,
    workspaces,
    subjects,
    conversations,
    selectedWorkspaceId,
    selectedSubjectId,
    selectedConversationId,
    theme,
    setWorkspaces,
    setSubjects,
    setConversations,
    setSelectedWorkspaceId,
    setSelectedSubjectId,
    setSelectedConversationId,
    setTheme,
    setMessages,
    resetSession,
  } = useAppStore();
  const [workspaceName, setWorkspaceName] = useState("");
  const [subjectName, setSubjectName] = useState("");

  const visibleSubjects = useMemo(
    () => subjects.filter((subject) => subject.workspace_id === selectedWorkspaceId),
    [subjects, selectedWorkspaceId],
  );

  async function createWorkspace(event: FormEvent) {
    event.preventDefault();
    if (!token || !workspaceName.trim()) return;

    const workspace = await api.createWorkspace(token, workspaceName.trim());
    setWorkspaces([workspace, ...workspaces]);
    setSelectedWorkspaceId(workspace.id);
    setWorkspaceName("");
  }

  async function createSubject(event: FormEvent) {
    event.preventDefault();
    if (!token || !selectedWorkspaceId || !subjectName.trim()) return;

    const subject = await api.createSubject(token, subjectName.trim(), selectedWorkspaceId);
    setSubjects([subject, ...subjects]);
    setSelectedSubjectId(subject.id);
    setSubjectName("");
  }

  async function openConversation(id: string) {
    if (!token) return;
    setSelectedConversationId(id);
    const history = await api.messages(token, id);
    setMessages(history);
  }

  async function removeConversation(id: string) {
    if (!token) return;
    await api.deleteConversation(token, id);
    setConversations(conversations.filter((conversation) => conversation.id !== id));
    if (selectedConversationId === id) {
      setSelectedConversationId(null);
      setMessages([]);
    }
  }

  return (
    <aside className="flex min-h-0 flex-col gap-4 border-r border-line/70 bg-panel/65 p-4 dark:border-white/10 dark:bg-black/20">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-brand/80">FlowDocs</p>
          <h1 className="text-lg font-semibold text-foreground dark:text-white">Research OS</h1>
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            title={theme === "dark" ? "Light mode" : "Dark mode"}
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          <Button variant="ghost" size="sm" onClick={resetSession}>Logout</Button>
        </div>
      </div>

      <section className="grid gap-2">
        <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-[0.18em] text-muted">
          <UsersRound className="h-3.5 w-3.5" /> Workspaces
        </div>
        <form onSubmit={createWorkspace} className="flex gap-2">
          <Input
            value={workspaceName}
            onChange={(event) => setWorkspaceName(event.target.value)}
            placeholder="New workspace"
          />
          <Button type="submit" size="icon" aria-label="Create workspace">
            <Plus className="h-4 w-4" />
          </Button>
        </form>
        <div className="grid max-h-36 gap-1 overflow-y-auto">
          {workspaces.map((workspace) => (
            <button
              key={workspace.id}
              onClick={() => setSelectedWorkspaceId(workspace.id)}
              className={`rounded-lg px-3 py-2 text-left text-sm transition ${
                selectedWorkspaceId === workspace.id
                  ? "bg-brand/15 text-brand"
                  : "text-muted hover:bg-subtle/60 hover:text-foreground dark:text-slate-300 dark:hover:bg-white/[0.07] dark:hover:text-white"
              }`}
            >
              {workspace.name}
            </button>
          ))}
        </div>
      </section>

      <section className="grid gap-2">
        <div className="text-xs font-medium uppercase tracking-[0.18em] text-muted">Subjects</div>
        <form onSubmit={createSubject} className="flex gap-2">
          <Input
            value={subjectName}
            onChange={(event) => setSubjectName(event.target.value)}
            placeholder="New subject"
            disabled={!selectedWorkspaceId}
          />
          <Button type="submit" size="icon" disabled={!selectedWorkspaceId} aria-label="Create subject">
            <Plus className="h-4 w-4" />
          </Button>
        </form>
        <div className="grid max-h-40 gap-1 overflow-y-auto">
          {visibleSubjects.map((subject) => (
            <button
              key={subject.id}
              onClick={() => setSelectedSubjectId(subject.id)}
              className={`rounded-lg px-3 py-2 text-left text-sm transition ${
                selectedSubjectId === subject.id
                  ? "bg-mint/15 text-mint"
                  : "text-muted hover:bg-subtle/60 hover:text-foreground dark:text-slate-300 dark:hover:bg-white/[0.07] dark:hover:text-white"
              }`}
            >
              {subject.name}
            </button>
          ))}
        </div>
      </section>

      <section className="min-h-0 flex-1">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-[0.18em] text-muted">
            <MessageSquare className="h-3.5 w-3.5" /> Conversations
          </div>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => {
              setSelectedConversationId(null);
              setMessages([]);
            }}
            disabled={!selectedSubjectId}
          >
            New
          </Button>
        </div>
        <div className="grid max-h-full gap-2 overflow-y-auto pr-1">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`group rounded-xl border p-3 transition ${
                selectedConversationId === conversation.id
                  ? "border-brand/35 bg-brand/10"
                  : "border-line/70 bg-card/70 hover:bg-subtle/40 dark:border-white/10 dark:bg-white/[0.035] dark:hover:bg-white/[0.065]"
              }`}
            >
              <button className="w-full text-left" onClick={() => openConversation(conversation.id)}>
                <div className="line-clamp-1 text-sm font-medium text-foreground dark:text-slate-100">{conversation.title}</div>
                <div className="mt-1 line-clamp-2 text-xs leading-5 text-muted">
                  {conversation.latest_message_preview ?? "No messages yet"}
                </div>
                <div className="mt-2 text-[11px] text-muted/80">
                  {conversation.message_count} messages · {formatRelativeTime(conversation.latest_activity)}
                </div>
              </button>
              <Button
                variant="ghost"
                size="icon"
                className="mt-2 hidden h-7 w-7 text-muted group-hover:inline-flex"
                onClick={() => removeConversation(conversation.id)}
                aria-label="Delete conversation"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          ))}
        </div>
      </section>
    </aside>
  );
}
