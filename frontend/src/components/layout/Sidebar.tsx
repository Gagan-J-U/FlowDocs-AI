import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  BookOpen,
  FileText,
  GitCompareArrows,
  Hash,
  MessageSquare,
  Moon,
  Network,
  PanelLeftClose,
  PanelLeftOpen,
  Settings,
  Sun,
  Users,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { api } from "../../lib/api";
import { cn, formatRelativeTime } from "../../lib/utils";
import { useAppStore } from "../../store/app-store";
import { useUiStore } from "../../store/ui-store";
import type { AppRoute } from "../../types";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { NotificationBell } from "../notifications/NotificationCenter";

const workspaceNav: { route: AppRoute; label: string; icon: typeof MessageSquare; path: string }[] = [
  { route: "subjects", label: "Subjects", icon: BookOpen, path: "/subjects" },
  { route: "chat", label: "Conversations", icon: MessageSquare, path: "/chat" },
  { route: "documents", label: "Documents", icon: FileText, path: "/documents" },
  { route: "comparisons", label: "Comparisons", icon: GitCompareArrows, path: "/comparisons" },
  { route: "research", label: "Research Network", icon: Network, path: "/research" },
];

export function Sidebar() {
  const {
    token,
    workspaces,
    subjects,
    selectedWorkspaceId,
    selectedSubjectId,
    theme,
    setWorkspaces,
    setSelectedWorkspaceId,
    setSelectedSubjectId,
    setTheme,
    resetSession,
  } = useAppStore();
  const {
    sidebarCollapsed,
    toggleSidebarCollapsed,
    setActiveRoute,
  } = useUiStore();

  const [workspaceName, setWorkspaceName] = useState("");

  const visibleSubjects = useMemo(
    () => subjects.filter((subject) => subject.workspace_id === selectedWorkspaceId),
    [subjects, selectedWorkspaceId],
  );

  async function createWorkspace(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !workspaceName.trim()) return;
    const workspace = await api.createWorkspace(token, workspaceName.trim());
    setWorkspaces([workspace, ...workspaces]);
    setSelectedWorkspaceId(workspace.id);
    setWorkspaceName("");
  }

  const widthClass = sidebarCollapsed ? "w-[72px]" : "w-[280px]";

  return (
    <aside className={cn("flex h-full min-h-0 flex-col border-r border-line bg-panel transition-all duration-300", widthClass)}>
      <div className="flex items-center justify-between gap-2 border-b border-line px-3 py-3">
        {!sidebarCollapsed && (
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-brand">FlowDocs</p>
            <h1 className="text-base font-semibold text-foreground">AI</h1>
          </div>
        )}
        <Button variant="ghost" size="icon" onClick={toggleSidebarCollapsed} aria-label="Toggle sidebar">
          {sidebarCollapsed ? <PanelLeftOpen className="h-4 w-4" /> : <PanelLeftClose className="h-4 w-4" />}
        </Button>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-2 py-3">
        <section className="mb-4">
          {!sidebarCollapsed && (
            <p className="mb-2 px-2 text-[11px] font-semibold uppercase tracking-wide text-muted">Workspaces</p>
          )}
          {!sidebarCollapsed && (
            <form onSubmit={createWorkspace} className="mb-2 flex gap-2 px-1">
              <Input value={workspaceName} onChange={(e) => setWorkspaceName(e.target.value)} placeholder="New workspace" />
              <Button type="submit" size="icon" aria-label="Create workspace">+</Button>
            </form>
          )}
          <div className="grid gap-0.5">
            {workspaces.map((workspace) => (
              <button
                key={workspace.id}
                onClick={() => setSelectedWorkspaceId(workspace.id)}
                className={cn(
                  "flex items-center gap-2 rounded-lg px-2 py-2 text-left text-sm transition",
                  selectedWorkspaceId === workspace.id
                    ? "bg-brand/10 text-brand"
                    : "text-muted hover:bg-subtle/60 hover:text-foreground",
                )}
                title={workspace.name}
              >
                <Users className="h-4 w-4 shrink-0" />
                {!sidebarCollapsed && <span className="truncate">{workspace.name}</span>}
              </button>
            ))}
          </div>
        </section>

        {selectedWorkspaceId && (
          <section className="mb-4">
            {!sidebarCollapsed && (
              <p className="mb-2 px-2 text-[11px] font-semibold uppercase tracking-wide text-muted">Workspace</p>
            )}
            <div className="grid gap-0.5">
              {workspaceNav.map(({ label, icon: Icon, path }) => (
                <NavLink
                  key={path}
                  to={path}
                  onClick={() => setActiveRoute(path.replace("/", "") as AppRoute)}
                  className={({ isActive }) => cn(
                    "flex items-center gap-2 rounded-lg px-2 py-2 text-sm transition",
                    isActive
                      ? "bg-brand/10 text-brand"
                      : "text-muted hover:bg-subtle/60 hover:text-foreground",
                  )}
                  title={label}
                >
                  <Icon className="h-4 w-4 shrink-0" />
                  {!sidebarCollapsed && label}
                </NavLink>
              ))}
              <NavLink
                to="/members"
                className={({ isActive }) => cn(
                  "flex items-center gap-2 rounded-lg px-2 py-2 text-sm transition",
                  isActive ? "bg-brand/10 text-brand" : "text-muted hover:bg-subtle/60 hover:text-foreground",
                )}
                title="Members"
              >
                <Users className="h-4 w-4 shrink-0" />
                {!sidebarCollapsed && "Members"}
              </NavLink>
            </div>
          </section>
        )}

        {!sidebarCollapsed && selectedWorkspaceId && visibleSubjects.length > 0 && (
          <section className="mb-4 px-1">
            <p className="mb-2 px-1 text-[11px] font-semibold uppercase tracking-wide text-muted">Quick subjects</p>
            <div className="grid gap-0.5">
              {visibleSubjects.slice(0, 5).map((subject) => (
                <button
                  key={subject.id}
                  onClick={() => setSelectedSubjectId(subject.id)}
                  className={cn(
                    "rounded-lg px-2 py-1.5 text-left text-xs transition",
                    selectedSubjectId === subject.id
                      ? "bg-mint/10 text-mint"
                      : "text-muted hover:bg-subtle/60 hover:text-foreground",
                  )}
                >
                  {subject.name}
                </button>
              ))}
            </div>
          </section>
        )}
      </div>

      <div className="border-t border-line p-2">
        <div className="grid gap-0.5">
          <NavLink
            to="/messages"
            className={({ isActive }) => cn(
              "flex items-center gap-2 rounded-lg px-2 py-2 text-sm transition",
              isActive ? "bg-brand/10 text-brand" : "text-muted hover:bg-subtle/60",
            )}
            title="Messages"
          >
            <MessageSquare className="h-4 w-4" />
            {!sidebarCollapsed && "Messages"}
          </NavLink>
          <NavLink
            to="/workspace-chat"
            className={({ isActive }) => cn(
              "flex items-center gap-2 rounded-lg px-2 py-2 text-sm transition",
              isActive ? "bg-brand/10 text-brand" : "text-muted hover:bg-subtle/60",
            )}
            title="Workspace chat"
          >
            <Hash className="h-4 w-4" />
            {!sidebarCollapsed && "Workspace chat"}
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) => cn(
              "flex items-center gap-2 rounded-lg px-2 py-2 text-sm transition",
              isActive ? "bg-brand/10 text-brand" : "text-muted hover:bg-subtle/60",
            )}
            title="Settings"
          >
            <Settings className="h-4 w-4" />
            {!sidebarCollapsed && "Settings"}
          </NavLink>
        </div>

        <div className={cn("mt-2 flex items-center gap-1", sidebarCollapsed ? "flex-col" : "justify-between px-1")}>
          <NotificationBell />
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          {!sidebarCollapsed && (
            <Button variant="ghost" size="sm" onClick={resetSession}>Logout</Button>
          )}
        </div>
      </div>
    </aside>
  );
}

export function ConversationSidebar() {
  const {
    token,
    conversations,
    selectedConversationId,
    pinnedConversationIds,
    selectedSubjectId,
    setSelectedConversationId,
    setMessages,
    setConversations,
    togglePinConversation,
  } = useAppStore();
  const { conversationSearch, setConversationSearch } = useUiStore();

  const filteredConversations = useMemo(() => {
    const query = conversationSearch.trim().toLowerCase();
    const sorted = [...conversations].sort((a, b) => {
      const aPinned = pinnedConversationIds.includes(a.id);
      const bPinned = pinnedConversationIds.includes(b.id);
      if (aPinned !== bPinned) return aPinned ? -1 : 1;
      return new Date(b.latest_activity).getTime() - new Date(a.latest_activity).getTime();
    });
    if (!query) return sorted;
    return sorted.filter((item) =>
      item.title.toLowerCase().includes(query) ||
      (item.latest_message_preview ?? "").toLowerCase().includes(query),
    );
  }, [conversations, conversationSearch, pinnedConversationIds]);

  async function openConversation(id: string) {
    if (!token) return;
    setSelectedConversationId(id);
    const history = await api.messages(token, id);
    setMessages(history);
  }

  async function removeConversation(id: string) {
    if (!token) return;
    await api.deleteConversation(token, id);
    setConversations(conversations.filter((c) => c.id !== id));
    if (selectedConversationId === id) {
      setSelectedConversationId(null);
      setMessages([]);
    }
  }

  return (
    <aside className="flex h-full min-h-0 w-[280px] flex-col border-r border-line bg-panel">
      <div className="border-b border-line p-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-foreground">Conversations</h2>
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
        <Input
          value={conversationSearch}
          onChange={(e) => setConversationSearch(e.target.value)}
          placeholder="Search conversations..."
          className="mt-2"
        />
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto p-2">
        {filteredConversations.map((conversation) => {
          const pinned = pinnedConversationIds.includes(conversation.id);
          return (
            <motion.div
              key={conversation.id}
              layout
              className={cn(
                "group mb-1 rounded-xl border p-3 transition",
                selectedConversationId === conversation.id
                  ? "border-brand/30 bg-brand/8"
                  : "border-line bg-card hover:bg-subtle/30",
              )}
            >
              <button className="w-full text-left" onClick={() => openConversation(conversation.id)}>
                <div className="flex items-center gap-2">
                  {pinned && <span className="text-[10px] text-brand">PIN</span>}
                  <div className="line-clamp-1 flex-1 text-sm font-medium text-foreground">{conversation.title}</div>
                </div>
                <p className="mt-1 line-clamp-2 text-xs leading-5 text-muted">
                  {conversation.latest_message_preview ?? "No messages yet"}
                </p>
                <p className="mt-2 text-[11px] text-muted/80">
                  {conversation.message_count} messages · {formatRelativeTime(conversation.latest_activity)}
                </p>
              </button>
              <div className="mt-2 flex gap-1 opacity-0 transition group-hover:opacity-100">
                <Button size="sm" variant="ghost" onClick={() => togglePinConversation(conversation.id)}>
                  {pinned ? "Unpin" : "Pin"}
                </Button>
                <Button size="sm" variant="ghost" onClick={() => removeConversation(conversation.id)}>
                  Delete
                </Button>
              </div>
            </motion.div>
          );
        })}
        {!filteredConversations.length && (
          <p className="px-2 py-8 text-center text-sm text-muted">No conversations yet</p>
        )}
      </div>
    </aside>
  );
}
