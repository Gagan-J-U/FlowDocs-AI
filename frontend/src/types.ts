export type Provider = "ollama" | "openai" | "gemini";
export type PromptMode = "default" | "teaching" | "debate";
export type Role = "user" | "assistant" | "system";

export interface Workspace {
  id: string;
  name: string;
  created_at: string;
}

export interface Subject {
  id: string;
  name: string;
  workspace_id: string;
  created_at: string;
}

export interface DocumentRecord {
  id: string;
  filename: string;
  stored_filename: string;
  file_path: string;
  mime_type: string | null;
  file_size: number | null;
  subject_id: string;
  uploaded_at: string;
}

export interface Citation {
  index?: number;
  section_title?: string;
  section?: string;
  pages?: number[] | string;
  page?: number;
  snippet?: string;
  text?: string;
  document_id?: string;
  document?: string;
  filename?: string;
  [key: string]: unknown;
}

export interface ConversationSummary {
  id: string;
  title: string;
  created_at: string;
  latest_message_preview: string | null;
  latest_activity: string;
  message_count: number;
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  citations: Citation[];
  created_at: string;
  streaming?: boolean;
}
