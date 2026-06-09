import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
    Citation,
    ComparisonResult,
    ConversationSummary,
    DocumentRecord,
    Message,
    PromptMode,
    Provider,
    Subject,
    Theme,
    Workspace,
} from "../types";

export interface User {
  id: string;
  username?: string;
  email?: string;
  avatar?: string;
}

interface AppState {
  token: string | null;
  user: User | null;
  workspaces: Workspace[];
  subjects: Subject[];
  documents: DocumentRecord[];
  conversations: ConversationSummary[];
  messages: Message[];
  selectedWorkspaceId: string | null;
  selectedSubjectId: string | null;
  selectedConversationId: string | null;
  selectedCitation: Citation | null;
  comparisonResult: ComparisonResult | null;
  comparisonLoading: boolean;
  comparisonError: string | null;
  pinnedConversationIds: string[];
  provider: Provider;
  mode: PromptMode;
  theme: Theme;
  streaming: boolean;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  setWorkspaces: (workspaces: Workspace[]) => void;
  setSubjects: (subjects: Subject[]) => void;
  setDocuments: (documents: DocumentRecord[]) => void;
  setConversations: (conversations: ConversationSummary[]) => void;
  setMessages: (messages: Message[]) => void;
  appendMessage: (message: Message) => void;
  updateStreamingMessage: (content: string, citations?: Citation[], figures?: Message["referenced_figures"]) => void;
  setSelectedWorkspaceId: (id: string | null) => void;
  setSelectedSubjectId: (id: string | null) => void;
  setSelectedConversationId: (id: string | null) => void;
  setSelectedCitation: (citation: Citation | null) => void;
  setComparisonResult: (result: ComparisonResult | null) => void;
  setComparisonLoading: (loading: boolean) => void;
  setComparisonError: (error: string | null) => void;
  togglePinConversation: (id: string) => void;
  setProvider: (provider: Provider) => void;
  setMode: (mode: PromptMode) => void;
  setTheme: (theme: Theme) => void;
  setStreaming: (streaming: boolean) => void;
  resetSession: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      workspaces: [],
      subjects: [],
      documents: [],
      conversations: [],
      messages: [],
      selectedWorkspaceId: null,
      selectedSubjectId: null,
      selectedConversationId: null,
      selectedCitation: null,
      comparisonResult: null,
      comparisonLoading: false,
      comparisonError: null,
      pinnedConversationIds: [],
      provider: "ollama",
      mode: "default",
      theme: "dark",
      streaming: false,
      setToken: (token) => set({
        token,
        workspaces: [],
        subjects: [],
        documents: [],
        conversations: [],
        messages: [],
        selectedWorkspaceId: null,
        selectedSubjectId: null,
        selectedConversationId: null,
        selectedCitation: null,
        comparisonResult: null,
        comparisonLoading: false,
        comparisonError: null,
        streaming: false,
      }),
      setUser: (user) => set({ user }),
      setWorkspaces: (workspaces) => set({ workspaces }),
      setSubjects: (subjects) => set({ subjects }),
      setDocuments: (documents) => set({ documents }),
      setConversations: (conversations) => set({ conversations }),
      setMessages: (messages) => set({ messages }),
      appendMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
      updateStreamingMessage: (content, citations = [], figures = []) => set((state) => {
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
          referenced_figures: figures,
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
      setComparisonResult: (result) => set({ comparisonResult: result }),
      setComparisonLoading: (loading) => set({ comparisonLoading: loading }),
      setComparisonError: (error) => set({ comparisonError: error }),
      togglePinConversation: (id) => set((state) => ({
        pinnedConversationIds: state.pinnedConversationIds.includes(id)
          ? state.pinnedConversationIds.filter((item) => item !== id)
          : [...state.pinnedConversationIds, id],
      })),
      setProvider: (provider) => set({ provider }),
      setMode: (mode) => set({ mode }),
      setTheme: (theme) => set({ theme }),
      setStreaming: (streaming) => set({ streaming }),
      resetSession: () => set({
        token: null,
        user: null,
        workspaces: [],
        subjects: [],
        documents: [],
        conversations: [],
        messages: [],
        selectedWorkspaceId: null,
        selectedSubjectId: null,
        selectedConversationId: null,
        selectedCitation: null,
        comparisonResult: null,
        comparisonLoading: false,
        comparisonError: null,
        streaming: false,
      }),
    }),
    {
      name: "flowdocs-ai",
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        selectedWorkspaceId: state.selectedWorkspaceId,
        selectedSubjectId: state.selectedSubjectId,
        provider: state.provider,
        mode: state.mode,
        theme: state.theme,
        pinnedConversationIds: state.pinnedConversationIds,
      }),
    },
  ),
);
