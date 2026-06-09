import type {
  ChatResult,
  ComparisonResult,
  ConversationSummary,
  DirectMessage,
  DocumentRecord,
  Message,
  PromptMode,
  Provider,
  ResearchProfile,
  Subject,
  Workspace,
  WorkspaceChatMessage,
  WorkspaceInvitation,
  WorkspaceMember,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function isAuthError(error: unknown) {
  return error instanceof ApiError && (error.status === 401 || error.status === 403);
}

function detailToMessage(detail: unknown, fallback: string) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") return item;
        if (item && typeof item === "object" && "msg" in item) return String(item.msg);
        return JSON.stringify(item);
      })
      .join("; ");
  }
  if (detail && typeof detail === "object") return JSON.stringify(detail);
  return fallback;
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
): Promise<T> {
  const headers = new Headers(options.headers);

  if (!(options.body instanceof FormData)) {
    if (!headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(detailToMessage(body.detail, response.statusText), response.status);
  }

  return response.json() as Promise<T>;
}

export const api = {
  baseUrl: API_BASE_URL,
  register(input: { username: string; email: string; password: string }) {
    return request<{ id: string; username: string; email: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(input),
    });
  },
  login(input: { email: string; password: string }) {
    const form = new URLSearchParams();
    form.set("username", input.email);
    form.set("password", input.password);

    return request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form,
    });
  },
  workspaces(token: string) {
    return request<Workspace[]>("/workspaces/", {}, token);
  },
  createWorkspace(token: string, name: string) {
    return request<Workspace>("/workspaces/", {
      method: "POST",
      body: JSON.stringify({ name }),
    }, token);
  },
  subjects(token: string) {
    return request<Subject[]>("/subjects/", {}, token);
  },
  createSubject(token: string, name: string, workspaceId: string) {
    return request<Subject>("/subjects/", {
      method: "POST",
      body: JSON.stringify({ name, workspace_id: workspaceId }),
    }, token);
  },
  documents(token: string, subjectId: string) {
    return request<DocumentRecord[]>(`/documents/subject/${subjectId}`, {}, token);
  },
  uploadDocument(
    token: string,
    subjectId: string,
    file: File,
    onProgress?: (progress: number) => void,
  ) {
    return new Promise<DocumentRecord>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const form = new FormData();
      form.append("file", file);

      xhr.open("POST", `${API_BASE_URL}/documents/upload/${subjectId}`);
      xhr.setRequestHeader("Authorization", `Bearer ${token}`);

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable && onProgress) {
          onProgress(Math.round((event.loaded / event.total) * 100));
        }
      };

      xhr.onload = () => {
        try {
          if (xhr.status >= 200 && xhr.status < 300) {
            onProgress?.(100);
            resolve(JSON.parse(xhr.responseText));
          } else {
            const body = JSON.parse(xhr.responseText || "{}");
            reject(new ApiError(detailToMessage(body.detail, "Upload failed"), xhr.status));
          }
        } catch {
          reject(new ApiError(xhr.responseText || "Upload failed", xhr.status || 500));
        }
      };
      xhr.onerror = () => reject(new ApiError("Upload failed", xhr.status || 500));
      xhr.send(form);
    });
  },
  dmConversations(token: string) {
    return request<{
      id: string;
      other_user_id: string;
      other_username: string;
      latest_message: string | null;
      latest_message_at: string | null;
    }[]>("/dm/conversations", {}, token).then((conversations) =>
      conversations.map((conversation) => ({
        id: conversation.id,
        participant_id: conversation.other_user_id,
        participant_name: conversation.other_username,
        last_message: conversation.latest_message ?? "",
        last_message_at: conversation.latest_message_at ?? "",
        unread_count: 0,
        online: conversation.online ?? false,
      })),
    );
  },
  dmMessages(token: string, conversationId: string) {
    return request<DirectMessage[]>(`/dm/conversations/${conversationId}/messages`, {}, token);
  },
  sendDmMessage(token: string, conversationId: string, content: string) {
    return request<DirectMessage>(`/dm/conversations/${conversationId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }, token);
  },
  createDmConversation(token: string, userId: string) {
    return request<{ id: string; other_user_id: string; other_username: string }>(`/dm/conversations`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }, token);
  },
  searchUsers(token: string, query: string) {
    const params = new URLSearchParams({ q: query });
    return request<{ id: string; username: string; email: string }[]>(`/users/search?${params}`, {}, token);
  },
  me(token: string) {
    return request<{ id: string; username: string; email: string }>("/users/me", {}, token);
  },
  workspaceChatMessages(token: string, workspaceId: string) {
    return request<WorkspaceChatMessage[]>(`/workspaces/${workspaceId}/chat`, {}, token);
  },
  sendWorkspaceChatMessage(token: string, workspaceId: string, content: string) {
    return request<WorkspaceChatMessage>(`/workspaces/${workspaceId}/chat`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }, token);
  },
  receivedWorkspaceInvitations(token: string) {
    return request<WorkspaceInvitation[]>(`/workspace-members/invitations/received`, {}, token);
  },
  chat(
    token: string,
    input: {
      workspaceId: string;
      subjectId: string;
      query: string;
      mode: PromptMode;
      provider: Provider;
      conversationId?: string | null;
      signal?: AbortSignal;
    },
  ) {
    return request<ChatResult>("/chat/", {
      method: "POST",
      signal: input.signal,
      body: JSON.stringify({
        workspace_id: input.workspaceId,
        subject_id: input.subjectId,
        query: input.query,
        mode: input.mode,
        provider: input.provider,
        conversation_id: input.conversationId,
      }),
    }, token);
  },
  compareDocuments(
    token: string,
    input: {
      workspaceId: string;
      subjectId: string;
      documentAId: string;
      documentBId: string;
      query: string;
      provider: Provider;
    },
  ) {
    return request<ComparisonResult>("/comparison/", {
      method: "POST",
      body: JSON.stringify({
        workspace_id: input.workspaceId,
        subject_id: input.subjectId,
        document_a_id: input.documentAId,
        document_b_id: input.documentBId,
        query: input.query,
        provider: input.provider,
      }),
    }, token);
  },
  conversations(token: string, workspaceId: string) {
    return request<ConversationSummary[]>(`/conversations/workspace/${workspaceId}`, {}, token);
  },
  messages(token: string, conversationId: string) {
    return request<Message[]>(`/conversations/${conversationId}/messages`, {}, token);
  },
  deleteConversation(token: string, conversationId: string) {
    return request<{ id: string; deleted: boolean }>(`/conversations/${conversationId}`, {
      method: "DELETE",
    }, token);
  },
  researchProfile(token: string) {
    return request<ResearchProfile>("/research/profile", {}, token);
  },
  updateResearchProfile(token: string, payload: Partial<ResearchProfile>) {
    return request<ResearchProfile>("/research/profile", {
      method: "PUT",
      body: JSON.stringify(payload),
    }, token);
  },
  researchProfileByUser(userId: string) {
    return request<ResearchProfile>(`/research/profile/${userId}`, {});
  },
  discoverResearchers(token: string, query: string, topK = 10) {
    const params = new URLSearchParams({ query, top_k: String(topK) });
    return request<ResearchProfile[]>(`/research/discover?${params}`, {}, token);
  },
  workspaceMembers(token: string, workspaceId: string) {
    return request<WorkspaceMember[]>(`/workspace-members/${workspaceId}/members`, {}, token);
  },
  workspaceInvitations(token: string, workspaceId: string) {
    return request<WorkspaceInvitation[]>(`/workspace-members/${workspaceId}/invitations`, {}, token);
  },
  inviteWorkspaceMember(
    token: string,
    workspaceId: string,
    input: { email: string; role: string },
  ) {
    return request<WorkspaceInvitation>(`/workspace-members/${workspaceId}/invite`, {
      method: "POST",
      body: JSON.stringify(input),
    }, token);
  },
  updateMemberRole(
    token: string,
    workspaceId: string,
    userId: string,
    role: string,
  ) {
    return request<WorkspaceMember>(`/workspace-members/${workspaceId}/members/${userId}/role`, {
      method: "PUT",
      body: JSON.stringify({ role }),
    }, token);
  },
  removeWorkspaceMember(token: string, workspaceId: string, userId: string) {
    return request<{ message: string }>(`/workspace-members/${workspaceId}/members/${userId}`, {
      method: "DELETE",
    }, token);
  },
  acceptInvitation(token: string, inviteToken: string) {
    return request<{ message: string }>("/workspace-members/accept", {
      method: "POST",
      body: JSON.stringify({ token: inviteToken }),
    }, token);
  },
  notifications(
    token: string
  ) {
    return request(
      "/notifications",
      {},
      token
    );
  },
  
  markNotificationRead(
    token: string,
    notificationId: string
  ) {
    return request(
      `/notifications/${notificationId}/read`,
      {
        method: "POST"
      },
      token
    );
  },
};
