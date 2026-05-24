import type {
  ConversationSummary,
  DocumentRecord,
  Message,
  Subject,
  Workspace,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
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
    throw new ApiError(body.detail ?? response.statusText, response.status);
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
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(new ApiError(xhr.responseText || "Upload failed", xhr.status));
        }
      };
      xhr.onerror = () => reject(new ApiError("Upload failed", xhr.status || 500));
      xhr.send(form);
    });
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
};
