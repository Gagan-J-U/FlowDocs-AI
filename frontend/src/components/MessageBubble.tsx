import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";
import { Check, Copy, ExternalLink, FileText, Image as ImageIcon, Quote } from "lucide-react";
import { useState } from "react";
import type { Citation, FigureReference, Message } from "../types";
import { api } from "../lib/api";
import { cn } from "../lib/utils";
import { useAppStore } from "../store/app-store";
import { Button } from "./ui/button";

function titleFor(citation: Citation) {
  return citation.section_title ?? citation.section ?? citation.filename ?? "Source";
}

function figureTitle(figure: FigureReference, index: number) {
  return figure.figure_id ? `Figure ${figure.figure_id}` : `Figure ${index + 1}`;
}

function figureImageSrc(figure: FigureReference) {
  const raw = figure.image_url ?? figure.url ?? figure.image_path;

  if (!raw) return null;
  if (/^(https?:|data:|blob:)/i.test(raw)) return raw;

  const normalized = raw.startsWith("/") ? raw : `/${raw}`;
  return `${api.baseUrl}${normalized}`;
}

function ReferencedFigures({ figures }: { figures: FigureReference[] }) {
  const [failedImages, setFailedImages] = useState<Record<string, boolean>>({});

  if (!figures.length) return null;

  return (
    <section className="mt-4 border-t border-line/70 pt-3 dark:border-white/10">
      <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.16em] text-muted">
        <ImageIcon className="h-3.5 w-3.5" />
        Referenced figures
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        {figures.map((figure, index) => {
          const title = figureTitle(figure, index);
          const imageSrc = figureImageSrc(figure);
          const imageKey = figure.figure_id ?? imageSrc ?? String(index);
          const canShowImage = Boolean(imageSrc) && !failedImages[imageKey];

          return (
            <article
              key={`${title}-${index}`}
              className="overflow-hidden rounded-lg border border-line/75 bg-panel/80 dark:border-white/10 dark:bg-black/15"
            >
              {canShowImage ? (
                <button
                  type="button"
                  className="block w-full bg-subtle/40 text-left dark:bg-white/[0.035]"
                  onClick={() => imageSrc && window.open(imageSrc, "_blank", "noopener,noreferrer")}
                  aria-label={`Open ${title}`}
                >
                  <img
                    src={imageSrc ?? ""}
                    alt={String(figure.caption ?? title)}
                    loading="lazy"
                    className="h-44 w-full object-contain"
                    onError={() => setFailedImages((current) => ({ ...current, [imageKey]: true }))}
                  />
                </button>
              ) : (
                <div className="flex h-28 items-center justify-center bg-subtle/45 text-muted dark:bg-white/[0.035]">
                  <FileText className="h-6 w-6" />
                </div>
              )}

              <div className="space-y-2 p-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h4 className="truncate text-sm font-semibold text-foreground dark:text-slate-100">{title}</h4>
                    {figure.page_number !== null && figure.page_number !== undefined && (
                      <p className="mt-0.5 text-xs text-muted">Page {String(figure.page_number)}</p>
                    )}
                  </div>
                  {imageSrc && (
                    <Button
                      type="button"
                      size="icon"
                      variant="ghost"
                      onClick={() => window.open(imageSrc, "_blank", "noopener,noreferrer")}
                      aria-label={`Open ${title}`}
                    >
                      <ExternalLink className="h-3.5 w-3.5" />
                    </Button>
                  )}
                </div>
                {figure.caption && (
                  <p className="line-clamp-3 text-xs leading-5 text-muted">{figure.caption}</p>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

export function MessageBubble({ message }: { message: Message }) {
  const setSelectedCitation = useAppStore((state) => state.setSelectedCitation);
  const [copied, setCopied] = useState(false);
  const isUser = message.role === "user";
  const figures = message.referenced_figures?.length ? message.referenced_figures : message.figures ?? [];

  async function copy() {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <article className={cn("group flex gap-3", isUser && "justify-end")}>
      {!isUser && (
        <div className="mt-1 flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-brand/15 text-brand">
          <Quote className="h-4 w-4" />
        </div>
      )}
      <div
        className={cn(
          "max-w-[min(760px,100%)] rounded-2xl border px-4 py-3 shadow-panel",
          isUser
            ? "border-brand/20 bg-brand/90 text-white dark:text-ink"
            : "border-line/70 bg-card/80 text-foreground dark:border-white/10 dark:bg-white/[0.055] dark:text-slate-100",
        )}
      >
        <div
          className={cn(
            "markdown-stream prose max-w-none text-sm leading-7 prose-p:text-foreground dark:prose-invert",
            isUser && "prose-p:text-white dark:prose-p:text-ink",
          )}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeSanitize]}
            components={{
              code({ className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                return match ? (
                  <SyntaxHighlighter
                    style={oneDark}
                    language={match[1]}
                    PreTag="div"
                    customStyle={{ margin: "0.8rem 0", background: "rgba(0,0,0,0.45)" }}
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content || (message.streaming ? "Thinking..." : "")}
          </ReactMarkdown>
        </div>

        {!isUser && Boolean(message.citations?.length) && (
          <div className="mt-3 flex flex-wrap gap-2">
            {message.citations.map((citation, index) => (
              <button
                key={`${titleFor(citation)}-${index}`}
                onClick={() => setSelectedCitation(citation)}
                title={String(citation.snippet ?? citation.text ?? titleFor(citation))}
                className="rounded-full border border-brand/20 bg-brand/10 px-2.5 py-1 text-xs text-brand transition hover:bg-brand/20"
              >
                [{index + 1}] {titleFor(citation)}
              </button>
            ))}
          </div>
        )}

        {!isUser && <ReferencedFigures figures={figures} />}

        <div className="mt-2 flex justify-end opacity-0 transition group-hover:opacity-100">
          <Button size="sm" variant="ghost" onClick={copy}>
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
            {copied ? "Copied" : "Copy"}
          </Button>
        </div>
      </div>
    </article>
  );
}
