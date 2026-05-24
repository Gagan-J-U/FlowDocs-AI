import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  Citation,
  ConversationSummary,
  DocumentRecord,
  Message,
  PromptMode,
  Provider,
  Subject,
  Workspace,
} from "../types";

interface AppState {
  token: string | null;
  workspaces: Workspace[];
  subjects: Subject[];
  documents: DocumentRecord[];
  conversations: ConversationSummary[];
  messages: Message[];
  selectedWorkspaceId: string | null;
  selectedSubjectId: string | null;
  selectedConversationId: string | null;
  selectedCitation: Citation | null;
  provider: Provider;
  mode: PromptMode;
  streaming: boolean;
  setToken: (token: string | null) => void;
  setWorkspaces: (workspaces: Workspace[]) => void;
  setSubjects: (subjects: Subject[]) => void;
  setDocuments: (documents: DocumentRecord[]) => void;
  setConversations: (conversations: ConversationSummary[]) => void;
  setMessages: (messages: Message[]) => void;
  appendMessage: (message: Message) => void;
  updateStreamingMessage: (content: string, citations?: Citation[]) => void;
  setSelectedWorkspaceId: (id: string | null) => void;
  setSelectedSubjectId: (id: string | null) => void;
  setSelectedConversationId: (id: string | null) => void;
  setSelectedCitation: (citation: Citation | null) => void;
  setProvider: (provider: Provider) => void;
  setMode: (mode: PromptMode) => void;
  setStreaming: (streaming: boolean) => void;
  resetSession: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      token: null,
      workspaces: [],
      subjects: [],
      documents: [],
      conversations: [],
      messages: [],
      selectedWorkspaceId: null,
      selectedSubjectId: null,
      selectedConversationId: null,
      selectedCitation: null,
      provider: "ollama",
      mode: "default",
      streaming: false,
      setToken: (token) => set({ token }),
      setWorkspaces: (workspaces) => set({ workspaces }),
      setSubjects: (subjects) => set({ subjects }),
      setDocuments: (documents) => set({ documents }),
      setConversations: (conversations) => set({ conversations }),
      setMessages: (messages) => set({ messages }),
      appendMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
      updateStreamingMessage: (content, citations = []) => set((state) => {
        const messages = [...state.messages];
        let lastIndex = -1;

        for (let index = messages.length - 1; index >= 0; index -= 1) {
          if (messages[index].streaming) {
            lastIndex = index;
            break;
          }
        }

        if (lastIndex === -1) {
          return { messages };
        }

        messages[lastIndex] = {
          ...messages[lastIndex],
          content,
          citations,
        };

        return { messages };
      }),
      setSelectedWorkspaceId: (id) => set({
        selectedWorkspaceId: id,
        selectedSubjectId: null,
        selectedConversationId: null,
        selectedCitation: null,
        messages: [],
      }),
      setSelectedSubjectId: (id) => set({
        selectedSubjectId: id,
        selectedConversationId: null,
        selectedCitation: null,
        messages: [],
      }),
      setSelectedConversationId: (id) => set({ selectedConversationId: id, selectedCitation: null }),
      setSelectedCitation: (citation) => set({ selectedCitation: citation }),
      setProvider: (provider) => set({ provider }),
      setMode: (mode) => set({ mode }),
      setStreaming: (streaming) => set({ streaming }),
      resetSession: () => set({
        token: null,
        workspaces: [],
        subjects: [],
        documents: [],
        conversations: [],
        messages: [],
        selectedWorkspaceId: null,
        selectedSubjectId: null,
        selectedConversationId: null,
        selectedCitation: null,
        streaming: false,
      }),
    }),
    {
      name: "flowdocs-ai",
      partialize: (state) => ({
        token: state.token,
        selectedWorkspaceId: state.selectedWorkspaceId,
        selectedSubjectId: state.selectedSubjectId,
        provider: state.provider,
        mode: state.mode,
      }),
    },
  ),
);
