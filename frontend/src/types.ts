export type Provider = "ollama" | "openai" | "gemini";
export type PromptMode = "default" | "teaching" | "debate";
export type Role = "user" | "assistant" | "system";
export type Theme = "dark" | "light";
export type WorkspaceMemberRole = "owner" | "editor" | "viewer";
export type DocumentViewMode = "grid" | "list";
export type ConversationFilter = "all" | "pinned" | "recent";

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
  page_count?: number | null;
  processing_status?: "pending" | "processing" | "ready" | "failed";
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

export interface FigureReference {
  figure_id?: string;
  page_number?: number | string | null;
  caption?: string | null;
  image_path?: string | null;
  image_url?: string | null;
  url?: string | null;
  width?: number | null;
  height?: number | null;
  [key: string]: unknown;
}

export interface ConversationSummary {
  id: string;
  title: string;
  created_at: string;
  latest_message_preview: string | null;
  latest_activity: string;
  message_count: number;
  pinned?: boolean;
  subject_id?: string;
}

export interface Message {
  id: string;
  role: Role;
  content: string;
  citations: Citation[];
  figures?: FigureReference[];
  referenced_figures?: FigureReference[];
  created_at: string;
  streaming?: boolean;
}

export interface ChatResult {
  conversation_id: string;
  query?: string;
  answer: string;
  citations?: Citation[];
  sources?: Citation[];
  figures?: FigureReference[];
  referenced_figures?: FigureReference[];
}

export interface ComparisonResult {
  query?: string;
  answer?: string;
  result?: string;
  comparison?: string;
  document_a_id?: string;
  document_b_id?: string;
  document_a_summary?: string;
  document_b_summary?: string;
  document_a_sources?: Citation[];
  document_b_sources?: Citation[];
  sources?: Citation[];
  figures?: FigureReference[];
  [key: string]: unknown;
}

export interface ResearchProfile {
  id?: string;
  user_id: string;
  username?: string;
  bio?: string | null;
  institution?: string | null;
  department?: string | null;
  skills?: string | null;
  interests?: string | null;
  github_url?: string | null;
  linkedin_url?: string | null;
  website_url?: string | null;
  visibility?: string;
  created_at?: string;
  updated_at?: string;
  similarity_score?: number;
}

export interface WorkspaceMember {
  id: string;
  user_id: string;
  workspace_id: string;
  role: WorkspaceMemberRole;
  email?: string;
  username?: string;
  joined_at?: string;
}

export interface WorkspaceInvitation {
  id: string;
  workspace_id?: string;
  workspace_name?: string;
  email: string;
  role: WorkspaceMemberRole;
  token?: string;
  created_at?: string;
}

export interface DirectMessageThread {
  id: string;
  participant_id: string;
  participant_name: string;
  participant_avatar?: string;
  last_message: string;
  last_message_at: string;
  unread_count: number;
  online?: boolean;
  typing?: boolean;
}

export interface DirectMessage {
  id: string;
  thread_id: string;
  sender_id: string;
  sender_name?: string;
  sender_avatar?: string;
  content: string;
  created_at: string;
  read_at?: string | null;
  message_status?: "sending" | "sent" | "delivered" | "read";
}

export interface WorkspaceChannel {
  id: string;
  name: string;
  description?: string;
  unread_count?: number;
  last_message_at?: string;
}

export interface WorkspaceChatMessage {
  id: string;
  channel_id: string;
  author_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  created_at: string;
  message_status?: "sending" | "sent" | "delivered" | "read";
  is_edited?: boolean;
}

export interface AppNotification {
  id: string;
  category: "mentions" | "invitations" | "messages" | "research";
  title: string;
  body: string;
  read: boolean;
  created_at: string;
  href?: string;
}

export type AppRoute =
  | "chat"
  | "subjects"
  | "documents"
  | "comparisons"
  | "research"
  | "members"
  | "messages"
  | "workspace-chat"
  | "settings";
