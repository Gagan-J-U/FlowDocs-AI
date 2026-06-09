import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bell, X } from "lucide-react";
import { fetchMockNotifications } from "../../lib/mock/social";
import { cn, formatRelativeTime } from "../../lib/utils";
import type { AppNotification } from "../../types";
import { useUiStore } from "../../store/ui-store";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { Skeleton } from "../ui/skeleton";
import { api }
  from "../../lib/api";

import { useAppStore }
  from "../../store/app-store";

const categoryLabels = {
  mentions: "Mentions",
  invitations: "Invitations",
  messages: "Messages",
  research: "Research",
} as const;

export function NotificationBell() {
  const { notificationsOpen, setNotificationsOpen } = useUiStore();
  const [notifications, setNotifications] = useState<AppNotification[]>([]);
  const [loading, setLoading] = useState(false);
  const unread = notifications.filter((item) => !item.read).length;

  useEffect(() => {
    if (!notificationsOpen) return;
    setLoading(true);
    const token =
    useAppStore(
      state => state.token
    );
    api.notifications(token)
  }, [notificationsOpen]);

  return (
    <>
      <Button
        variant="ghost"
        size="icon"
        onClick={() => setNotificationsOpen(!notificationsOpen)}
        aria-label="Notifications"
        className="relative"
      >
        <Bell className="h-4 w-4" />
        {unread > 0 && (
          <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-mint px-1 text-[10px] font-semibold text-ink">
            {unread}
          </span>
        )}
      </Button>

      <AnimatePresence>
        {notificationsOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-ink/20"
              onClick={() => setNotificationsOpen(false)}
            />
            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 16 }}
              className="fixed bottom-4 right-4 top-4 z-50 w-full max-w-md overflow-hidden rounded-2xl border border-line bg-card shadow-panel"
            >
              <div className="flex items-center justify-between border-b border-line px-4 py-3">
                <div>
                  <h2 className="text-sm font-semibold text-foreground">Notifications</h2>
                  <p className="text-xs text-muted">{unread} unread</p>
                </div>
                <Button variant="ghost" size="icon" onClick={() => setNotificationsOpen(false)}>
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <div className="max-h-full overflow-y-auto p-2">
                {loading && (
                  <div className="space-y-2 p-2">
                    <Skeleton className="h-16" />
                    <Skeleton className="h-16" />
                  </div>
                )}
                {!loading && notifications.map((item) => (
                  <button
                    key={item.id}
                    className={cn(
                      "mb-1 w-full rounded-xl border p-3 text-left transition hover:bg-subtle/30",
                      item.read ? "border-line bg-panel" : "border-brand/20 bg-brand/5",
                    )}
                    onClick={() => setNotifications((current) =>
                      current.map((n) => (n.id === item.id ? { ...n, read: true } : n)),
                    )}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <Badge variant="outline">{categoryLabels[item.category]}</Badge>
                      <span className="text-[11px] text-muted">{formatRelativeTime(item.created_at)}</span>
                    </div>
                    <p className="mt-2 text-sm font-medium text-foreground">{item.title}</p>
                    <p className="mt-1 text-xs leading-5 text-muted">{item.body}</p>
                  </button>
                ))}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
