import { MessageSquare, Search, Send } from "lucide-react";
import { FormEvent, useEffect, useRef, useState } from "react";
import { DMMessageBubble } from "../components/DMMessageBubble";
import { Avatar } from "../components/ui/avatar";
import { Button } from "../components/ui/button";
import { EmptyState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { Skeleton } from "../components/ui/skeleton";
import { api } from "../lib/api";
import { cn, formatRelativeTime } from "../lib/utils";
import { useAppStore } from "../store/app-store";
import type { DirectMessage, DirectMessageThread } from "../types";
import {
  createWebSocketService
} from "../lib/websocket";

export function MessagesPage() {
  const token = useAppStore((state) => state.token);
  const user = useAppStore((state) => state.user);
  const [threads, setThreads] = useState<DirectMessageThread[]>([]);
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<DirectMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [search, setSearch] = useState("");
  const [userSearch, setUserSearch] = useState("");
  const [userResults, setUserResults] = useState<{ id: string; username: string; email: string }[]>([]);
  const [showUserSearch, setShowUserSearch] = useState(false);
  const [searchingUsers, setSearchingUsers] = useState(false);
  const [loading, setLoading] = useState(true);
  const [typing, setTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userSearchError, setUserSearchError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const wsRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!token) return;

    setLoading(true);
    let cancelled = false;

    api.dmConversations(token)
      .then((data) => {
        if (cancelled) return;

        setThreads(data);
        if (!selectedThreadId && data[0]) {
          setSelectedThreadId(data[0].id);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load conversations");
          setThreads([]);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token, selectedThreadId]);

  useEffect(() => {
    if (!token || !selectedThreadId) {
      setMessages([]);
      return;
    }

    let cancelled = false;

    api.dmMessages(token, selectedThreadId)
      .then((data) => {
        if (!cancelled) {
          setMessages(data);
          setTyping(Boolean(threads.find((t) => t.id === selectedThreadId)?.typing));
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load messages");
          setMessages([]);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token, selectedThreadId, threads]);


  useEffect(() => {
    if (!token || !selectedThreadId) return;
  
    const protocol =
      window.location.protocol === "https:"
        ? "wss"
        : "ws";
  
    const host =
      import.meta.env.VITE_API_BASE_URL
        ?.replace(/^https?:\/\//, "")
        || window.location.host;
  
    const websocketUrl =
      `${protocol}://${host}/ws/dm/${selectedThreadId}?token=${token}`;
  
    const socket =
      createWebSocketService(
        websocketUrl
      );
  
    wsRef.current = socket;
  
    socket
      .connect()
      .then(() => {
  
        console.log(
          "DM websocket connected"
        );
  
        socket.on(
          "message",
          (message: any) => {
        
            console.log(
              "Realtime message:",
              message
            );
        
            const realtimeMessage: DirectMessage = {
        
              id: message.id,
        
              thread_id:
                message.conversation_id,
        
              sender_id:
                message.sender_id,
        
              sender_name:
                message.sender_name ??
                "User",
        
              sender_avatar:
                undefined,
        
              content:
                message.content,
        
              created_at:
                message.created_at,
        
              message_status:
                "delivered"
            };
        
            setMessages(
              current => {
        
                const exists =
                  current.some(
                    m =>
                      m.id ===
                      realtimeMessage.id
                  );
        
                if (exists) {
                  return current;
                }
        
                return [
                  ...current,
                  realtimeMessage
                ];
              }
            );
          }
        );
      })
      .catch(console.error);
  
    return () => {
  
      socket.disconnect();
    };
  
  }, [
    token,
    selectedThreadId
  ]);
  
  async function searchUsers() {
    if (!token || !userSearch.trim()) return;
    setSearchingUsers(true);
    setUserSearchError(null);
    try {
      const results = await api.searchUsers(token, userSearch.trim());
      setUserResults(Array.isArray(results) ? results : []);
    } catch (err) {
      setUserSearchError(err instanceof Error ? err.message : "Search failed");
      setUserResults([]);
    } finally {
      setSearchingUsers(false);
    }
  }

  async function startDmWithUser(userId: string) {
    if (!token) return;
    setSearchingUsers(true);
    try {
      const conversation = await api.createDmConversation(token, userId);
      const data = await api.dmConversations(token);
      setThreads(data);
      setSelectedThreadId(conversation.id);
      setShowUserSearch(false);
      setUserSearch("");
      setUserResults([]);
    } catch (err) {
      setUserSearchError(err instanceof Error ? err.message : "Unable to start conversation");
    } finally {
      setSearchingUsers(false);
    }
  }

  const filteredThreads = threads.filter((thread) =>
    thread.participant_name.toLowerCase().includes(search.toLowerCase()),
  );

  const selectedThread = threads.find((t) => t.id === selectedThreadId);

  async function sendMessage(
    event: FormEvent
  ) {
  
    event.preventDefault();
  
    if (
      !draft.trim() ||
      !selectedThreadId
    ) {
      return;
    }
  
    const content =
      draft.trim();
  
    setDraft("");
  
    console.log(
      "SENDING WS:",
      content
    );
  
    wsRef.current?.send(
      content
    );
  }

  if (loading) {
    return (
      <div className="flex h-full p-4 gap-4">
        <Skeleton className="h-full w-72" />
        <Skeleton className="h-full flex-1" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-0 flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-2xl">
          <EmptyState icon={MessageSquare} title="Messages unavailable" description={error} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-0 flex-1 overflow-hidden">
      <aside className="flex w-full max-w-xs flex-col border-r border-line bg-panel">
        <div className="border-b border-line p-3">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="text-sm font-semibold text-foreground">Inbox</h1>
              <p className="mt-1 text-xs text-muted">Search your threads or message a new researcher.</p>
            </div>
            <Button size="sm" onClick={() => setShowUserSearch((current) => !current)}>
              {showUserSearch ? "Hide new message" : "New message"}
            </Button>
          </div>
          <div className="relative mt-3">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search threads..." className="pl-9" />
          </div>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto">
          {showUserSearch && (
            <div className="space-y-3 border-b border-line/60 px-3 py-3">
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
                <Input
                  value={userSearch}
                  onChange={(e) => setUserSearch(e.target.value)}
                  placeholder="Search users to message..."
                  className="pl-9"
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      void searchUsers();
                    }
                  }}
                />
              </div>
              <div className="flex flex-wrap gap-2">
                <Button type="button" variant="secondary" size="sm" onClick={() => void searchUsers()} disabled={searchingUsers || !userSearch.trim()}>
                  Search users
                </Button>
                {userSearchError && <span className="text-xs text-destructive">{userSearchError}</span>}
              </div>
              <div className="space-y-2">
                {searchingUsers && <p className="text-xs text-muted">Searching…</p>}
                {userResults.map((user) => (
                  <div key={user.id} className="flex items-center justify-between gap-3 rounded-2xl border border-line bg-panel p-3">
                    <div>
                      <p className="text-sm font-medium text-foreground">{user.username || user.email}</p>
                      <p className="text-xs text-muted">{user.email}</p>
                    </div>
                    <Button type="button" size="sm" onClick={() => void startDmWithUser(user.id)}>
                      Message
                    </Button>
                  </div>
                ))}
                {!searchingUsers && userSearch.trim() && !userResults.length && (
                  <p className="text-xs text-muted">No users found.</p>
                )}
              </div>
            </div>
          )}
          {filteredThreads.map((thread) => (
            <button
              key={thread.id}
              onClick={() => setSelectedThreadId(thread.id)}
              className={cn(
                "flex w-full items-start gap-3 border-b border-line/60 px-3 py-3 text-left transition hover:bg-subtle/30",
                selectedThreadId === thread.id && "bg-brand/5",
              )}
            >
              <Avatar name={thread.participant_name} online={thread.online} />
              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate text-sm font-medium text-foreground">{thread.participant_name}</p>
                  {thread.unread_count > 0 && (
                    <span className="rounded-full bg-mint px-1.5 text-[10px] font-semibold text-ink">{thread.unread_count}</span>
                  )}
                </div>
                <p className="mt-0.5 line-clamp-1 text-xs text-muted">{thread.last_message}</p>
                <p className="mt-1 text-[11px] text-muted/80">{formatRelativeTime(thread.last_message_at)}</p>
              </div>
            </button>
          ))}
        </div>
      </aside>

      <section className="flex min-h-0 min-w-0 flex-1 flex-col bg-card">
        {selectedThread ? (
          <>
            <header className="flex items-center gap-3 border-b border-line px-4 py-3">
              <Avatar name={selectedThread.participant_name} online={selectedThread.online} />
              <div className="flex-1">
                <h2 className="text-sm font-semibold text-foreground">{selectedThread.participant_name}</h2>
                <p className="text-xs text-muted">{selectedThread.online ? "● Online" : "● Offline"}</p>
              </div>
            </header>
            <div className="min-h-0 flex-1 overflow-y-auto p-4 space-y-1">
              {messages.length === 0 ? (
                <p className="text-xs text-muted text-center py-8">No messages yet. Start the conversation!</p>
              ) : (
                messages.map((message, index) => {
                  const isOwn = message.sender_id === user?.id;
                  const showAvatar = !isOwn && (index === 0 || messages[index - 1]?.sender_id !== message.sender_id);
                  const showSenderName = !isOwn && index === 0;

                  return (
                    <DMMessageBubble
                      key={message.id}
                      message={message}
                      isOwn={isOwn}
                      showAvatar={showAvatar}
                      showSenderName={showSenderName}
                      showTime={true}
                    />
                  );
                })
              )}
              {typing && (
                <div className="flex gap-2 items-center text-xs text-muted">
                  <div className="flex gap-1">
                    <span className="h-2 w-2 rounded-full bg-current animate-pulse"></span>
                    <span className="h-2 w-2 rounded-full bg-current animate-pulse delay-100"></span>
                    <span className="h-2 w-2 rounded-full bg-current animate-pulse delay-200"></span>
                  </div>
                  Typing…
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <form onSubmit={sendMessage} className="flex gap-2 border-t border-line p-3">
              <Input
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
                placeholder="Write a message..."
                className="flex-1"
              />
              <Button type="submit" variant="primary" size="icon" disabled={!draft.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </>
        ) : (
          <EmptyState icon={MessageSquare} title="Select a conversation" description="Choose a thread from your inbox." />
        )}
      </section>
    </div>
  );
}
