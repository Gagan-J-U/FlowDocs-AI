import { cn } from "../../lib/utils";

const variants = {
  default: "bg-subtle/80 text-foreground",
  brand: "bg-brand/12 text-brand",
  mint: "bg-mint/12 text-mint",
  outline: "border border-line text-muted",
} as const;

export function Badge({
  children,
  variant = "default",
  className,
}: {
  children: React.ReactNode;
  variant?: keyof typeof variants;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide",
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
