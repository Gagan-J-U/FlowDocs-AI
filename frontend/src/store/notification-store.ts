import { create } from "zustand";
import type { AppNotification } from "../types";

interface NotificationStore {
  notifications: AppNotification[];
  addNotification: (notification: Omit<AppNotification, "id" | "created_at">) => void;
  removeNotification: (id: string) => void;
  markAsRead: (id: string) => void;
  clearNotifications: () => void;
}

export const useNotificationStore = create<NotificationStore>((set) => ({
  notifications: [],
  addNotification: (notification) =>
    set((state) => ({
      notifications: [
        {
          ...notification,
          id: `notif-${Date.now()}-${Math.random()}`,
          created_at: new Date().toISOString(),
        },
        ...state.notifications,
      ],
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
  markAsRead: (id) =>
    set((state) => ({
      notifications: state.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n,
      ),
    })),
  clearNotifications: () => set({ notifications: [] }),
}));

export function createNotificationMessage(
  category: AppNotification["category"],
  title: string,
  body: string,
  href?: string,
): Omit<AppNotification, "id" | "created_at"> {
  return {
    category,
    title,
    body,
    read: false,
    ...(href && { href }),
  };
}

// Toast-like notifications for temporary display
export function notifyUser(
  title: string,
  message: string,
  type: "success" | "error" | "info" = "info",
) {
  // This can be expanded to integrate with a toast library
  console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
}
