import { Check, CheckCheck } from "lucide-react";
import { cn, formatMessageTime } from "../lib/utils";
import { useAppStore } from "../store/app-store";
import type { DirectMessage } from "../types";
import { Avatar } from "./ui/avatar";

interface DMMessageBubbleProps {
  message: DirectMessage;
  isOwn: boolean;
  showAvatar?: boolean;
  showSenderName?: boolean;
  showTime?: boolean;
}

export function DMMessageBubble({
  message,
  isOwn,
  showAvatar = true,
  showSenderName = false,
  showTime = true,
}: DMMessageBubbleProps) {
  const user = useAppStore((state) => state.user);

  return (
    <div className={cn("flex gap-2 mb-2", isOwn && "flex-row-reverse justify-end")}>
      {showAvatar && !isOwn && (
        <div className="flex-shrink-0">
          <Avatar name={message.sender_name || "User"} size="sm" />
        </div>
      )}

      {isOwn && (
        <div className="flex-shrink-0 w-8" />
      )}

      <div className={cn("flex flex-col", isOwn && "items-end")}>
        {showSenderName && !isOwn && (
          <p className="text-xs text-muted mb-1">{message.sender_name || "User"}</p>
        )}

        <div
          className={cn(
            "max-w-xs px-3 py-2 rounded-lg break-words",
            isOwn
              ? "bg-blue-500 text-white rounded-br-none"
              : "bg-gray-200 text-gray-900 rounded-bl-none dark:bg-gray-700 dark:text-white",
          )}
        >
          <p className="text-sm leading-6 whitespace-pre-wrap">{message.content}</p>
        </div>

        <div className={cn("flex items-center gap-1 mt-1", isOwn ? "flex-row-reverse" : "flex-row")}>
          {showTime && (
            <span className="text-[11px] text-muted">{formatMessageTime(message.created_at)}</span>
          )}
          {isOwn && message.message_status && (
            <div className="text-[11px]">
              {message.message_status === "sending" && (
                <span className="text-muted">●</span>
              )}
              {message.message_status === "sent" && (
                <Check className="h-3 w-3 text-muted" />
              )}
              {message.message_status === "delivered" && (
                <CheckCheck className="h-3 w-3 text-muted" />
              )}
              {message.message_status === "read" && (
                <CheckCheck className="h-3 w-3 text-blue-500" />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
