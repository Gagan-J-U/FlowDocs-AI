import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, RefreshCcw, Send, Square } from "lucide-react";
import { api } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { Message, PromptMode, Provider } from "../types";
import { Button } from "./ui/button";
import { MessageBubble } from "./MessageBubble";
import { ConversationSidebar } from "./layout/Sidebar";
import { EmptyState } from "./ui/empty-state";
import { streamChat } from "../lib/stream";

const providers: Provider[] = ["ollama", "openai", "gemini"];
const modes: PromptMode[] = ["default", "teaching", "debate"];

export function ChatPanel() {
  const {
    token,
    workspaces,
    subjects,
    messages,
    selectedWorkspaceId,
    selectedSubjectId,
    selectedConversationId,
    provider,
    mode,
    streaming,
    setProvider,
    setMode,
    appendMessage,
    updateStreamingMessage,
    setSelectedConversationId,
    setConversations,
    setStreaming,
  } = useAppStore();
  const [query, setQuery] = useState("");
  const [error, setError] = useState<string | null>(null);
  const viewportRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const latestUserQuery = useMemo(
    () => [...messages].reverse().find((message) => message.role === "user")?.content ?? "",
    [messages],
  );

  const workspace = workspaces.find((item) => item.id === selectedWorkspaceId);
  const subject = subjects.find((item) => item.id === selectedSubjectId);

  useEffect(() => {
    viewportRef.current?.scrollTo({
      top: viewportRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  async function refreshConversations(conversationId?: string) {
    if (!token || !selectedWorkspaceId) return;
    const next = await api.conversations(token, selectedWorkspaceId);
    setConversations(next);
    if (conversationId) setSelectedConversationId(conversationId);
  }

  async function submitMessage(event?: FormEvent, retryText?: string) {
    event?.preventDefault();
    const content = (retryText ?? query).trim();
    if (!content || !token || !selectedWorkspaceId || !selectedSubjectId || streaming) return;

    setError(null);
    setQuery("");
    const controller = new AbortController();
    abortRef.current = controller;
    setStreaming(true);

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content,
      citations: [],
      created_at: new Date().toISOString(),
    };
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "",
      citations: [],
      referenced_figures: [],
      created_at: new Date().toISOString(),
      streaming: true,
    };

    appendMessage(userMessage);
    appendMessage(assistantMessage);

    try {
      let accumulated = "";

      await streamChat({
        token,
        workspaceId: selectedWorkspaceId,
        subjectId: selectedSubjectId,
        query: content,
        mode,
        provider,
        conversationId: selectedConversationId,
        signal: controller.signal,

        onConversation: (
          conversationId
        ) => {

          setSelectedConversationId(
            conversationId
          );
        },

        onToken: (
          token
        ) => {

          accumulated += token;

          updateStreamingMessage(
            accumulated
          );
        },

        onDone: async (
          payload
        ) => {
        
          updateStreamingMessage(
            accumulated,
            payload.citations ?? [],
            payload.referenced_figures?.length
              ? payload.referenced_figures
              : payload.figures ?? []
          );
        
          await refreshConversations(
            payload.conversation_id
          );
        },

        onError: (
          message
        ) => {

          setError(
            message
          );
        },
      });
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setError(err instanceof Error ? err.message : "Chat failed");
      }
    } finally {
      setStreaming(false);
      abortRef.current = null;
      useAppStore.setState((state) => ({
        messages: state.messages.map((message) => (
          message.streaming ? { ...message, streaming: false } : message
        )),
      }));
    }
  }

  function stopStream() {
    abortRef.current?.abort();
    setStreaming(false);
  }

  if (!selectedSubjectId) {
    return (
      <EmptyState
        icon={Bot}
        title="Select a subject"
        description="Choose a subject from the sidebar to start a grounded conversation."
      />
    );
  }

  return (
    <div className="flex min-h-0 flex-1">
      <div className="hidden min-h-0 md:flex">
        <ConversationSidebar />
      </div>

      <div className="flex min-h-0 min-w-0 flex-1 flex-col">
        <header className="flex flex-wrap items-center justify-between gap-3 border-b border-line bg-panel px-5 py-4">
          <div>
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-brand">
              <Bot className="h-3.5 w-3.5" /> {workspace?.name ?? "Workspace"}
            </div>
            <h2 className="mt-1 text-xl font-semibold text-foreground">{subject?.name ?? "Subject"}</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={provider}
              onChange={(event) => setProvider(event.target.value as Provider)}
              className="h-9 rounded-lg border border-line bg-card px-3 text-sm text-foreground outline-none focus:border-brand/50"
            >
              {providers.map((item) => <option key={item} value={item}>{item}</option>)}
            </select>
            <div className="flex rounded-lg border border-line bg-card p-1">
              {modes.map((item) => (
                <button
                  key={item}
                  onClick={() => setMode(item)}
                  className={`rounded-md px-3 py-1.5 text-xs capitalize transition ${
                    mode === item
                      ? "bg-brand/12 text-brand"
                      : "text-muted hover:text-foreground"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </header>

        <div ref={viewportRef} className="min-h-0 flex-1 overflow-y-auto px-4 py-6 md:px-8">
          <div className="mx-auto grid max-w-3xl gap-5">
            <AnimatePresence initial={false}>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                >
                  <MessageBubble message={message} />
                </motion.div>
              ))}
            </AnimatePresence>
            {!messages.length && (
              <div className="mt-16 text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-brand/20 bg-brand/8">
                  <Bot className="h-7 w-7 text-brand" />
                </div>
                <h3 className="mt-5 text-2xl font-semibold text-foreground">Ask across this subject</h3>
                <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-muted">
                  Grounded answers with citations, figure previews, and adaptive learning modes.
                </p>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="mx-auto mb-3 w-full max-w-3xl px-4">
            <div className="rounded-lg border border-red-400/25 bg-red-500/8 px-3 py-2 text-sm text-red-700 dark:text-red-200">
              {error}
            </div>
          </div>
        )}

        <form onSubmit={submitMessage} className="border-t border-line bg-panel p-4">
          <div className="mx-auto flex max-w-3xl items-end gap-3 rounded-2xl border border-line bg-card p-2">
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  void submitMessage();
                }
              }}
              placeholder="Ask FlowDocs..."
              className="min-h-12 max-h-36 flex-1 resize-none bg-transparent px-3 py-3 text-sm leading-6 text-foreground outline-none placeholder:text-muted"
              disabled={streaming}
            />
            {streaming ? (
              <Button type="button" variant="secondary" size="icon" onClick={stopStream} aria-label="Stop">
                <Square className="h-4 w-4" />
              </Button>
            ) : (
              <Button type="submit" variant="primary" size="icon" disabled={!query.trim()} aria-label="Send">
                <Send className="h-4 w-4" />
              </Button>
            )}
            <Button
              type="button"
              variant="ghost"
              size="icon"
              disabled={!latestUserQuery || streaming}
              onClick={() => void submitMessage(undefined, latestUserQuery)}
              aria-label="Regenerate"
            >
              <RefreshCcw className="h-4 w-4" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
