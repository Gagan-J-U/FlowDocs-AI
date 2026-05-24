import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, RefreshCcw, Send, Square } from "lucide-react";
import { api } from "../lib/api";
import { streamChat } from "../lib/stream";
import { useAppStore } from "../store/app-store";
import type { Message, PromptMode, Provider } from "../types";
import { Button } from "./ui/button";
import { MessageBubble } from "./MessageBubble";

const providers: Provider[] = ["ollama", "openai", "gemini"];
const modes: PromptMode[] = ["default", "teaching", "debate"];

export function ChatPanel() {
  const {
    token,
    workspaces,
    subjects,
    messages,
    conversations,
    selectedWorkspaceId,
    selectedSubjectId,
    selectedConversationId,
    provider,
    mode,
    streaming,
    setProvider,
    setMode,
    setMessages,
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
  const streamedText = useRef("");
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
    streamedText.current = "";
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
      created_at: new Date().toISOString(),
      streaming: true,
    };

    appendMessage(userMessage);
    appendMessage(assistantMessage);

    try {
      await streamChat({
        token,
        workspaceId: selectedWorkspaceId,
        subjectId: selectedSubjectId,
        query: content,
        mode,
        provider,
        conversationId: selectedConversationId,
        signal: controller.signal,
        onConversation: (conversationId) => setSelectedConversationId(conversationId),
        onToken: (tokenText) => {
          streamedText.current += tokenText;
          updateStreamingMessage(streamedText.current);
        },
        onDone: async (payload) => {
          updateStreamingMessage(streamedText.current, payload.citations ?? []);
          await refreshConversations(payload.conversation_id);
        },
        onError: (message) => setError(message),
      });
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setError(err instanceof Error ? err.message : "Streaming failed");
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

  return (
    <main className="flex min-h-0 flex-col">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 bg-black/10 px-5 py-4">
        <div>
          <div className="flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-brand/80">
            <Bot className="h-3.5 w-3.5" /> {workspace?.name ?? "No workspace"}
          </div>
          <h2 className="mt-1 text-xl font-semibold text-white">{subject?.name ?? "Select a subject"}</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          <select
            value={provider}
            onChange={(event) => setProvider(event.target.value as Provider)}
            className="h-9 rounded-lg border border-white/10 bg-white/[0.07] px-3 text-sm text-slate-100 outline-none"
          >
            {providers.map((item) => <option key={item} value={item}>{item}</option>)}
          </select>
          <div className="flex rounded-lg border border-white/10 bg-white/[0.045] p-1">
            {modes.map((item) => (
              <button
                key={item}
                onClick={() => setMode(item)}
                className={`rounded-md px-3 py-1.5 text-xs capitalize transition ${
                  mode === item ? "bg-white/12 text-white" : "text-slate-400 hover:text-white"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      </header>

      <div ref={viewportRef} className="min-h-0 flex-1 overflow-y-auto px-4 py-6 md:px-8">
        <div className="mx-auto grid max-w-4xl gap-5">
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
            <div className="mt-20 text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-brand/25 bg-brand/10">
                <Bot className="h-7 w-7 text-brand" />
              </div>
              <h3 className="mt-5 text-2xl font-semibold text-white">Ask across this subject</h3>
              <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
                Stream a grounded response, switch providers, or use teaching and debate modes for different reasoning styles.
              </p>
            </div>
          )}
        </div>
      </div>

      {error && (
        <div className="mx-auto mb-3 w-full max-w-4xl px-4">
          <div className="rounded-lg border border-red-400/25 bg-red-500/10 px-3 py-2 text-sm text-red-100">
            {error}
          </div>
        </div>
      )}

      <form onSubmit={submitMessage} className="border-t border-white/10 bg-ink/70 p-4 backdrop-blur-xl">
        <div className="mx-auto flex max-w-4xl items-end gap-3 rounded-2xl border border-white/10 bg-white/[0.065] p-2 shadow-panel">
          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                void submitMessage();
              }
            }}
            placeholder={selectedSubjectId ? "Ask FlowDocs..." : "Select a subject first"}
            className="min-h-12 max-h-36 flex-1 resize-none bg-transparent px-3 py-3 text-sm leading-6 text-slate-100 outline-none placeholder:text-slate-500"
            disabled={!selectedSubjectId || streaming}
          />
          {streaming ? (
            <Button type="button" variant="secondary" size="icon" onClick={stopStream} aria-label="Stop stream">
              <Square className="h-4 w-4" />
            </Button>
          ) : (
            <Button type="submit" variant="primary" size="icon" disabled={!query.trim() || !selectedSubjectId} aria-label="Send">
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
    </main>
  );
}
