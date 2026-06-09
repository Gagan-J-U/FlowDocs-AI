import { forwardRef } from "react";
import type { ButtonHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "icon";
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "secondary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-lg border transition disabled:pointer-events-none disabled:opacity-45",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/70",
          variant === "primary" && "border-brand/40 bg-brand text-white shadow-soft hover:bg-brand/90 dark:text-ink",
          variant === "secondary" && "border-line/80 bg-card/80 text-foreground hover:bg-subtle/50 dark:border-white/10 dark:bg-white/[0.07] dark:text-slate-100 dark:hover:bg-white/[0.11]",
          variant === "ghost" && "border-transparent bg-transparent text-muted hover:bg-subtle/60 hover:text-foreground dark:text-slate-300 dark:hover:bg-white/[0.08] dark:hover:text-white",
          variant === "danger" && "border-red-400/30 bg-red-500/15 text-red-700 hover:bg-red-500/25 dark:text-red-100",
          size === "sm" && "h-8 px-3 text-xs",
          size === "md" && "h-10 px-4 text-sm",
          size === "icon" && "h-9 w-9 p-0",
          className,
        )}
        {...props}
      />
    );
  },
);

Button.displayName = "Button";
