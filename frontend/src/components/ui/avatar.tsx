import { cn } from "../../lib/utils";

export function Avatar({
  name,
  className,
  online,
}: {
  name?: string;
  className?: string;
  online?: boolean;
}) {

  const safeName =
    name?.trim() || "User";

  const initials = safeName
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div
      className={cn(
        "relative inline-flex",
        className
      )}
    >
      <div
        className="
          flex
          h-9
          w-9
          items-center
          justify-center
          rounded-full
          bg-brand/15
          text-xs
          font-semibold
          text-brand
        "
      >
        {initials || "U"}
      </div>

      {online !== undefined && (
        <span
          className={cn(
            "absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full border-2 border-card",
            online
              ? "bg-mint"
              : "bg-muted/50"
          )}
        />
      )}
    </div>
  );
}