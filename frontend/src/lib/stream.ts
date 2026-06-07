import { api } from "./api";
import type { Citation, FigureReference, PromptMode, Provider } from "../types";

export interface StreamChatInput {
  token: string;
  workspaceId: string;
  subjectId: string;
  query: string;
  mode: PromptMode;
  provider: Provider;
  conversationId?: string | null;
  signal?: AbortSignal;
  onConversation: (conversationId: string, title: string) => void;
  onToken: (token: string) => void;
  onDone: (payload: {
    conversation_id: string;
    citations?: Citation[];
    figures?: FigureReference[];
    referenced_figures?: FigureReference[];
  }) => void;
  onError: (message: string) => void;
}

function parseSseBlock(block: string) {
  const event = block.match(/^event: (.+)$/m)?.[1] ?? "message";
  const dataLine = block
    .split("\n")
    .filter((line) => line.startsWith("data: "))
    .map((line) => line.slice(6))
    .join("\n");

  return {
    event,
    data: dataLine ? JSON.parse(dataLine) : {},
  };
}

export async function streamChat(input: StreamChatInput) {
  const response = await fetch(`${api.baseUrl}/chat-stream/`, {
    method: "POST",
    signal: input.signal,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${input.token}`,
    },
    body: JSON.stringify({
      workspace_id: input.workspaceId,
      subject_id: input.subjectId,
      query: input.query,
      mode: input.mode,
      provider: input.provider,
      conversation_id: input.conversationId,
    }),
  });

  if (!response.ok || !response.body) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? response.statusText);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const blocks = buffer.split("\n\n");
    buffer = blocks.pop() ?? "";

    for (const block of blocks) {
      if (!block.trim()) continue;

      const { event, data } = parseSseBlock(block);

      if (event === "conversation") {
        input.onConversation(data.conversation_id, data.title);
      }

      if (event === "token") {
        input.onToken(data.token);
      }

      if (event === "done") {
        input.onDone(data);
      }

      if (event === "error") {
        input.onError(data.message ?? "Stream failed");
      }
    }
  }
}
