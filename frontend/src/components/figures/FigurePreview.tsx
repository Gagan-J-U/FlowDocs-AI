import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X, ZoomIn, ZoomOut } from "lucide-react";
import type { FigureReference } from "../../types";
import { api } from "../../lib/api";
import { cn } from "../../lib/utils";
import { Button } from "../ui/button";

function figureImageSrc(figure: FigureReference) {
  const raw = figure.image_url ?? figure.url ?? figure.image_path;
  if (!raw) return null;
  if (/^(https?:|data:|blob:)/i.test(raw)) return raw;
  const normalized = raw.startsWith("/") ? raw : `/${raw}`;
  return `${api.baseUrl}${normalized}`;
}

export function FigureModal({
  figure,
  onClose,
}: {
  figure: FigureReference | null;
  onClose: () => void;
}) {
  const [zoom, setZoom] = useState(1);
  const imageSrc = figure ? figureImageSrc(figure) : null;

  useEffect(() => {
    setZoom(1);
  }, [figure]);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <AnimatePresence>
      {figure && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-ink/80 p-4 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.98, y: 4 }}
            transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="flex max-h-[90vh] w-full max-w-4xl flex-col overflow-hidden rounded-2xl border border-line bg-card shadow-panel"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-line px-4 py-3">
              <div>
                <h3 className="text-sm font-semibold text-foreground">
                  {figure.figure_id ? `Figure ${figure.figure_id}` : "Figure preview"}
                </h3>
                {figure.page_number !== null && figure.page_number !== undefined && (
                  <p className="text-xs text-muted">Page {String(figure.page_number)}</p>
                )}
              </div>
              <div className="flex items-center gap-1">
                <Button variant="ghost" size="icon" onClick={() => setZoom((value) => Math.max(0.5, value - 0.25))}>
                  <ZoomOut className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={() => setZoom((value) => Math.min(3, value + 0.25))}>
                  <ZoomIn className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={onClose}>
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <div className="min-h-0 flex-1 overflow-auto bg-subtle/30 p-4">
              {imageSrc ? (
                <img
                  src={imageSrc}
                  alt={String(figure.caption ?? "Figure")}
                  className={cn("mx-auto max-w-none transition-transform duration-200")}
                  style={{ transform: `scale(${zoom})`, transformOrigin: "center top" }}
                />
              ) : (
                <div className="grid h-64 place-items-center text-sm text-muted">Image unavailable</div>
              )}
            </div>
            {figure.caption && (
              <div className="border-t border-line px-4 py-3 text-sm leading-6 text-muted">
                {figure.caption}
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export function FigureThumbnail({
  figure,
  index,
  onExpand,
}: {
  figure: FigureReference;
  index: number;
  onExpand: () => void;
}) {
  const [failed, setFailed] = useState(false);
  const imageSrc = figureImageSrc(figure);
  const title = figure.figure_id ? `Figure ${figure.figure_id}` : `Figure ${index + 1}`;

  return (
    <article className="group overflow-hidden rounded-xl border border-line bg-panel transition hover:border-brand/30">
      <button type="button" className="block w-full text-left" onClick={onExpand}>
        {imageSrc && !failed ? (
          <img
            src={imageSrc}
            alt={String(figure.caption ?? title)}
            loading="lazy"
            className="h-40 w-full bg-subtle/40 object-contain transition group-hover:scale-[1.01]"
            onError={() => setFailed(true)}
          />
        ) : (
          <div className="flex h-40 items-center justify-center bg-subtle/30 text-xs text-muted">
            Preview unavailable
          </div>
        )}
      </button>
      <div className="space-y-1 p-3">
        <div className="flex items-center justify-between gap-2">
          <h4 className="truncate text-sm font-medium text-foreground">{title}</h4>
          {figure.page_number !== null && figure.page_number !== undefined && (
            <span className="text-xs text-muted">p.{String(figure.page_number)}</span>
          )}
        </div>
        {figure.caption && (
          <p className="line-clamp-2 text-xs leading-5 text-muted">{figure.caption}</p>
        )}
      </div>
    </article>
  );
}
