import { forwardRef } from "react";
import type { InputHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "h-10 w-full rounded-lg border border-line/80 bg-card/80 px-3 text-sm text-foreground",
        "placeholder:text-muted focus:border-brand/60 focus:outline-none focus:ring-2 focus:ring-brand/20",
        "dark:border-white/10 dark:bg-white/[0.06] dark:text-slate-100 dark:placeholder:text-slate-500",
        className,
      )}
      {...props}
    />
  ),
);

Input.displayName = "Input";
