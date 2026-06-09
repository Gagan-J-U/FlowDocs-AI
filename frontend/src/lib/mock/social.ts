import type {
  AppNotification,
  DirectMessage,
  DirectMessageThread,
  WorkspaceChannel,
  WorkspaceChatMessage,
} from "../../types";

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const mockNotifications: AppNotification[] = [
  {
    id: "n1",
    category: "invitations",
    title: "Workspace invitation",
    body: "You were invited to join Neural Systems Lab as Editor.",
    read: false,
    created_at: new Date(Date.now() - 3600000).toISOString(),
    href: "/members",
  },
  {
    id: "n2",
    category: "research",
    title: "Research match",
    body: "Dr. Elena Park shares 3 interests with your profile.",
    read: false,
    created_at: new Date(Date.now() - 7200000).toISOString(),
    href: "/research/discover",
  },
  {
    id: "n3",
    category: "messages",
    title: "New direct message",
    body: "Alex Chen: Can you review the retrieval pipeline notes?",
    read: true,
    created_at: new Date(Date.now() - 86400000).toISOString(),
    href: "/messages",
  },
  {
    id: "n4",
    category: "mentions",
    title: "Mentioned in #papers",
    body: "Jordan referenced you in workspace chat.",
    read: true,
    created_at: new Date(Date.now() - 172800000).toISOString(),
    href: "/workspace-chat",
  },
];

export const mockDirectThreads: DirectMessageThread[] = [
  {
    id: "t1",
    participant_id: "u1",
    participant_name: "Alex Chen",
    last_message: "Can you review the retrieval pipeline notes?",
    last_message_at: new Date(Date.now() - 1800000).toISOString(),
    unread_count: 2,
    online: true,
  },
  {
    id: "t2",
    participant_id: "u2",
    participant_name: "Elena Park",
    last_message: "Shared the updated benchmark results.",
    last_message_at: new Date(Date.now() - 86400000).toISOString(),
    unread_count: 0,
    online: false,
  },
];

export const mockDirectMessages: Record<string, DirectMessage[]> = {
  t1: [
    {
      id: "m1",
      thread_id: "t1",
      sender_id: "u1",
      content: "Hey — do you have a minute to look at the comparison output?",
      created_at: new Date(Date.now() - 3600000).toISOString(),
    },
    {
      id: "m2",
      thread_id: "t1",
      sender_id: "self",
      content: "Sure, I'll check it after this ingestion run finishes.",
      created_at: new Date(Date.now() - 3000000).toISOString(),
    },
    {
      id: "m3",
      thread_id: "t1",
      sender_id: "u1",
      content: "Can you review the retrieval pipeline notes?",
      created_at: new Date(Date.now() - 1800000).toISOString(),
    },
  ],
  t2: [
    {
      id: "m4",
      thread_id: "t2",
      sender_id: "u2",
      content: "Shared the updated benchmark results.",
      created_at: new Date(Date.now() - 86400000).toISOString(),
    },
  ],
};

export const mockWorkspaceChannels: WorkspaceChannel[] = [
  { id: "c1", name: "general", description: "Workspace-wide updates", unread_count: 3 },
  { id: "c2", name: "papers", description: "Paper discussion", unread_count: 0 },
  { id: "c3", name: "experiments", description: "Experiment logs", unread_count: 1 },
];

export const mockChannelMessages: Record<string, WorkspaceChatMessage[]> = {
  c1: [
    {
      id: "wc1",
      channel_id: "c1",
      author_id: "u3",
      author_name: "Jordan Lee",
      content: "Uploaded the new corpus to the Documents library.",
      created_at: new Date(Date.now() - 5400000).toISOString(),
    },
    {
      id: "wc2",
      channel_id: "c1",
      author_id: "self",
      author_name: "You",
      content: "Nice — I'll run comparisons against last week's set.",
      created_at: new Date(Date.now() - 4800000).toISOString(),
    },
  ],
  c2: [],
  c3: [],
};

export async function fetchMockNotifications() {
  await delay(300);
  return mockNotifications;
}

export async function fetchMockDirectThreads() {
  await delay(250);
  return mockDirectThreads;
}

export async function fetchMockDirectMessages(threadId: string) {
  await delay(200);
  return mockDirectMessages[threadId] ?? [];
}

export async function fetchMockWorkspaceChannels() {
  await delay(200);
  return mockWorkspaceChannels;
}

export async function fetchMockChannelMessages(channelId: string) {
  await delay(200);
  return mockChannelMessages[channelId] ?? [];
}
