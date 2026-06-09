import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";
import { Check, Copy, Quote } from "lucide-react";
import { useState } from "react";
import type { FigureReference, Message } from "../types";
import { cn } from "../lib/utils";
import { useAppStore } from "../store/app-store";
import { Button } from "./ui/button";
import { FigureModal, FigureThumbnail } from "./figures/FigurePreview";

function titleFor(citation: { section_title?: string; section?: string; filename?: string }) {
  return citation.section_title ?? citation.section ?? citation.filename ?? "Source";
}

export function MessageBubble({ message }: { message: Message }) {
  const setSelectedCitation = useAppStore((state) => state.setSelectedCitation);
  const [copied, setCopied] = useState(false);
  const [expandedFigure, setExpandedFigure] = useState<FigureReference | null>(null);
  const isUser = message.role === "user";
  const figures = message.referenced_figures?.length ? message.referenced_figures : message.figures ?? [];

  async function copy() {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <>
      <article className={cn("group flex gap-3", isUser && "justify-end")}>
        {!isUser && (
          <div className="mt-1 flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-brand/12 text-brand">
            <Quote className="h-4 w-4" />
          </div>
        )}
        <div
          className={cn(
            "max-w-[min(760px,100%)] rounded-2xl border px-4 py-3 shadow-soft",
            isUser
              ? "border-brand/20 bg-brand text-white dark:text-ink"
              : "border-line bg-card text-foreground",
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
                  className="rounded-full border border-brand/20 bg-brand/8 px-2.5 py-1 text-xs text-brand transition hover:bg-brand/15"
                >
                  [{index + 1}] {titleFor(citation)}
                </button>
              ))}
            </div>
          )}

          {!isUser && figures.length > 0 && (
            <section className="mt-4 border-t border-line pt-3">
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted">Referenced figures</p>
              <div className="grid gap-3 sm:grid-cols-2">
                {figures.map((figure, index) => (
                  <FigureThumbnail
                    key={`${figure.figure_id ?? index}`}
                    figure={figure}
                    index={index}
                    onExpand={() => setExpandedFigure(figure)}
                  />
                ))}
              </div>
            </section>
          )}

          <div className="mt-2 flex justify-end opacity-0 transition group-hover:opacity-100">
            <Button size="sm" variant="ghost" onClick={copy}>
              {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
              {copied ? "Copied" : "Copy"}
            </Button>
          </div>
        </div>
      </article>
      <FigureModal figure={expandedFigure} onClose={() => setExpandedFigure(null)} />
    </>
  );
}
