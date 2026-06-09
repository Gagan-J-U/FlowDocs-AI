import { MessageSquare, Send } from "lucide-react";
import { FormEvent, useEffect, useState, useRef } from "react";
import { Avatar } from "../components/ui/avatar";
import { Button } from "../components/ui/button";
import { EmptyState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { Skeleton } from "../components/ui/skeleton";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import { formatMessageTime } from "../lib/utils";
import type { WorkspaceChatMessage } from "../types";
import {
  createWebSocketService
} from "../lib/websocket";

export function WorkspaceChatPage() {
  const { token, selectedWorkspaceId } = useAppStore();
  const user = useAppStore((state) => state.user);
  const [messages, setMessages] = useState<WorkspaceChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<any>(
    null
  );

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {

    if (
      !token ||
      !selectedWorkspaceId
    ) {
      return;
    }
  
    const protocol =
  
      window.location.protocol ===
      "https:"
        ? "wss"
        : "ws";
  
    const host =
  
      import.meta.env
        .VITE_API_BASE_URL
  
        ?.replace(
          /^https?:\/\//,
          ""
        )
  
        || window.location.host;
  
    const websocketUrl =
  
      `${protocol}://${host}/ws/workspaces/${selectedWorkspaceId}?token=${token}`;
  
    const socket =
  
      createWebSocketService(
        websocketUrl
      );
  
    wsRef.current = socket;
  
    socket
      .connect()
      .then(() => {
  
        console.log(
          "Workspace websocket connected"
        );
  
        socket.on(
          "message",
          (message: any) => {
  
            console.log(
              "WORKSPACE REALTIME:",
              message
            );
  
            const realtimeMessage = {
  
              id:
                message.id,
  
              channel_id:
                message.workspace_id,
  
              author_id:
                message.sender_id,
  
                author_name:
                  message.sender_name ||
                  message.sender_username ||
                  "User",
  
              author_avatar:
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
    selectedWorkspaceId
  ]);
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!token || !selectedWorkspaceId) {
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    api.workspaceChatMessages(token, selectedWorkspaceId)
      .then((data) => {
        if (!cancelled) {
          setMessages(data);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load workspace chat");
          setMessages([]);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [token, selectedWorkspaceId]);

  async function sendMessage(
    event: FormEvent
  ) {
  
    event.preventDefault();
  
    if (
      !draft.trim()
    ) {
      return;
    }
  
    const content =
      draft.trim();
  
    setDraft("");
  
    wsRef.current?.send(
      content
    );
  }

  if (!selectedWorkspaceId) {
    return (
      <EmptyState
        icon={MessageSquare}
        title="No workspace selected"
        description="Choose a workspace before using the shared workspace chat."
      />
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
          <EmptyState icon={MessageSquare} title="Workspace chat unavailable" description={error} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-0 flex-1 overflow-hidden">
      <section className="flex min-h-0 min-w-0 flex-1 flex-col bg-card">
        <header className="flex items-center gap-3 border-b border-line px-4 py-3">
          <Avatar name="Workspace" />
          <div>
            <h2 className="text-sm font-semibold text-foreground">Workspace chat</h2>
            <p className="text-xs text-muted">Chat with your workspace collaborators in real time.</p>
          </div>
        </header>

        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-4">
          {messages.length === 0 ? (
            <p className="text-sm text-muted text-center py-8">No messages yet. Start the conversation!</p>
          ) : (
            messages.map((message, index) => {
              const isOwn = message.author_id === user?.id;
              const showAuthorInfo =
                index === 0 || messages[index - 1]?.author_id !== message.author_id;

              return (
                <div key={message.id} className="flex gap-3">
                  {showAuthorInfo && !isOwn && (
                    <Avatar name={message.author_name} size="sm" />
                  )}
                  {showAuthorInfo && isOwn && (
                    <div className="w-8 flex-shrink-0" />
                  )}
                  {!showAuthorInfo && (
                    <div className="w-8 flex-shrink-0" />
                  )}

                  <div className="flex-1 min-w-0">
                    {showAuthorInfo && (
                      <div className="flex items-baseline gap-2 mb-1">
                        <p className={`text-xs font-semibold ${isOwn ? "text-brand" : "text-foreground"}`}>
                          {isOwn ? "You" : message.author_name}
                        </p>
                        <p className="text-[11px] text-muted">{formatMessageTime(message.created_at)}</p>
                      </div>
                    )}
                    <div className={`rounded-lg px-3 py-2 inline-block max-w-md ${
                      isOwn
                        ? "bg-blue-500 text-white"
                        : "bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white"
                    }`}>
                      <p className="text-sm leading-6 whitespace-pre-wrap break-words">{message.content}</p>
                    </div>
                    {!showAuthorInfo && (
                      <p className="text-[11px] text-muted mt-1">{formatMessageTime(message.created_at)}</p>
                    )}
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="flex gap-2 border-t border-line p-3">
          <Input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Type a workspace message..."
            className="flex-1"
          />
          <Button type="submit" variant="primary" size="icon" disabled={!draft.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </section>
    </div>
  );
}



