import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AppRoute, DocumentViewMode } from "../types";

interface UiState {
  sidebarCollapsed: boolean;
  sidebarOpen: boolean;
  activeRoute: AppRoute;
  documentViewMode: DocumentViewMode;
  conversationSearch: string;
  notificationsOpen: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setSidebarOpen: (open: boolean) => void;
  setActiveRoute: (route: AppRoute) => void;
  setDocumentViewMode: (mode: DocumentViewMode) => void;
  setConversationSearch: (query: string) => void;
  setNotificationsOpen: (open: boolean) => void;
  toggleSidebarCollapsed: () => void;
}

export const useUiStore = create<UiState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      sidebarOpen: false,
      activeRoute: "chat",
      documentViewMode: "grid",
      conversationSearch: "",
      notificationsOpen: false,
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      setActiveRoute: (route) => set({ activeRoute: route }),
      setDocumentViewMode: (mode) => set({ documentViewMode: mode }),
      setConversationSearch: (query) => set({ conversationSearch: query }),
      setNotificationsOpen: (open) => set({ notificationsOpen: open }),
      toggleSidebarCollapsed: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
    }),
    {
      name: "flowdocs-ui",
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        documentViewMode: state.documentViewMode,
      }),
    },
  ),
);
