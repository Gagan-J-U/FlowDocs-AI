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
          variant === "primary" && "border-brand/40 bg-brand/90 text-ink shadow-glow hover:bg-brand",
          variant === "secondary" && "border-white/10 bg-white/[0.07] text-slate-100 hover:bg-white/[0.11]",
          variant === "ghost" && "border-transparent bg-transparent text-slate-300 hover:bg-white/[0.08]",
          variant === "danger" && "border-red-400/30 bg-red-500/15 text-red-100 hover:bg-red-500/25",
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
