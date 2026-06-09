import { Mail, UserPlus, Users } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { Avatar } from "../components/ui/avatar";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { EmptyState, ErrorState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { Skeleton } from "../components/ui/skeleton";
import { api, ApiError } from "../lib/api";
import { useAppStore } from "../store/app-store";
import type { WorkspaceInvitation, WorkspaceMember, WorkspaceMemberRole } from "../types";

const roles: WorkspaceMemberRole[] = ["owner", "editor", "viewer"];

export function MembersPage() {
  const { token, selectedWorkspaceId } = useAppStore();
  const [members, setMembers] = useState<WorkspaceMember[]>([]);
  const [invitations, setInvitations] = useState<WorkspaceInvitation[]>([]);
  const [receivedInvitations, setReceivedInvitations] = useState<WorkspaceInvitation[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingInvites, setLoadingInvites] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inviteOpen, setInviteOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState<WorkspaceMemberRole>("editor");
  const [inviteLoading, setInviteLoading] = useState(false);


  async function loadMembers() {
    if (!token || !selectedWorkspaceId) return;
    setLoading(true);
    setError(null);
    try {
      const [membersData, invitationsData] = await Promise.all([
        api.workspaceMembers(token, selectedWorkspaceId),
        api.workspaceInvitations(token, selectedWorkspaceId),
      ]);
      setMembers(membersData);
      setInvitations(invitationsData);
    } catch (err) {
      setError(err instanceof ApiError ? (err.message || `Failed (${err.status})`) : err instanceof Error ? err.message : "Failed to load members");
    } finally {
      setLoading(false);
    }
  }

  async function loadReceivedInvitations() {
    if (!token) return;
    setLoadingInvites(true);
    try {
      const received = await api.receivedWorkspaceInvitations(token);
      setReceivedInvitations(received);
    } catch (err) {
      setError(err instanceof ApiError ? (err.message || `Failed (${err.status})`) : err instanceof Error ? err.message : "Failed to load invitations");
    } finally {
      setLoadingInvites(false);
    }
  }


  useEffect(() => {
    void loadReceivedInvitations();
  }, [token]);

  useEffect(() => {
    void loadMembers();
  }, [token, selectedWorkspaceId]);

  async function invite(event: FormEvent) {
    event.preventDefault();
    if (!token || !selectedWorkspaceId || !inviteEmail.trim()) return;
    setInviteLoading(true);
    setError(null);
    try {
      await api.inviteWorkspaceMember(token, selectedWorkspaceId, {
        email: inviteEmail.trim(),
        role: inviteRole,
      });
      setInviteEmail("");
      setInviteOpen(false);
      await loadMembers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invite failed");
    } finally {
      setInviteLoading(false);
    }
  }

  async function acceptInvitation(tokenValue: string) {
    if (!token) return;
    setError(null);
    try {
      await api.acceptInvitation(token, tokenValue);
      await loadReceivedInvitations();
      if (selectedWorkspaceId) {
        await loadMembers();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Accept invitation failed");
    }
  }


  async function changeRole(userId: string, role: WorkspaceMemberRole) {
    if (!token || !selectedWorkspaceId) return;

    try {
      await api.updateMemberRole(token, selectedWorkspaceId, userId, role);
      await loadMembers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Role update failed");
    }
  }

  if (!selectedWorkspaceId) {
    return (
      <div className="min-h-0 flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-4xl">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-semibold text-foreground">Members</h1>
              <p className="mt-1 text-sm text-muted">Select a workspace to manage members, or accept invitations below.</p>
            </div>
          </div>
          {receivedInvitations.length > 0 ? (
            <div className="mt-6 rounded-2xl border border-line bg-card p-4">
              <div className="mb-3">
                <h2 className="text-sm font-semibold text-foreground">Invitations received</h2>
                <p className="text-xs text-muted">Accept an invitation to join a workspace.</p>
              </div>
              <div className="space-y-3">
                {receivedInvitations.map((invite) => (
                  <div key={invite.id} className="flex flex-col gap-3 rounded-xl border border-line bg-panel p-3 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-sm font-medium text-foreground">{invite.workspace_name ?? "Unknown workspace"}</p>
                      <p className="text-xs text-muted">Role: {invite.role} • Sent {new Date(invite.created_at ?? "").toLocaleDateString()}</p>
                    </div>
                    <Button type="button" onClick={() => void acceptInvitation(invite.token ?? "")}>Accept invite</Button>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <EmptyState icon={Users} title="Select a workspace" description="Choose a workspace to manage members." />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Members</h1>
            <p className="mt-1 text-sm text-muted">
              Manage workspace access and roles.
            </p>
          </div>
          <Button variant="primary" onClick={() => setInviteOpen(true)}>
            <UserPlus className="h-4 w-4" />
            Invite
          </Button>
        </div>
        {receivedInvitations.length > 0 && (
          <div className="mt-6 rounded-2xl border border-line bg-card p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <div>
                <h2 className="text-sm font-semibold text-foreground">Invitations received</h2>
                <p className="text-xs text-muted">Accept invitations for workspaces you have been invited to join.</p>
              </div>
            </div>
            <div className="space-y-3">
              {receivedInvitations.map((invite) => (
                <div key={invite.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-line bg-panel p-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">{invite.workspace_name ?? "Workspace invitation"}</p>
                    <p className="text-xs text-muted">Role: {invite.role} • Sent {new Date(invite.created_at ?? "").toLocaleDateString()}</p>
                  </div>
                  <Button type="button" size="sm" onClick={() => void acceptInvitation(invite.token ?? "")}>Accept</Button>
                </div>
              ))}
            </div>
          </div>
        )}

        {invitations.length > 0 && (
          <div className="mt-6 rounded-2xl border border-line bg-card p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <div>
                <h2 className="text-sm font-semibold text-foreground">Pending invitations</h2>
                <p className="text-xs text-muted">Invitations sent to collaborators that are still awaiting acceptance.</p>
              </div>
            </div>
            <div className="space-y-3">
              {invitations.map((invite) => (
                <div key={invite.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-line bg-panel p-3">
                  <div>
                    <p className="text-sm font-medium text-foreground">{invite.email}</p>
                    <p className="text-xs text-muted">Role: {invite.role} • Sent {new Date(invite.created_at ?? "").toLocaleDateString()}</p>
                  </div>
                  <div className="text-xs text-muted">Pending</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {error && <div className="mt-4"><ErrorState description={error} onRetry={() => void loadMembers()} /></div>}

        {loading ? (
          <div className="mt-6 space-y-2">
            <Skeleton className="h-16" />
            <Skeleton className="h-16" />
          </div>
        ) : (
          <div className="mt-6 space-y-2">
            {members.map((member) => (
              <div key={member.id} className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-line bg-panel p-4">
                <div className="flex items-center gap-3">
                  <Avatar name={member.username ?? member.email ?? "Member"} />
                  <div>
                    <p className="text-sm font-medium text-foreground">{member.username ?? member.email ?? member.user_id}</p>
                    <p className="text-xs text-muted">{member.email}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="brand">{member.role}</Badge>
                  {member.role !== "owner" && (
                    <select
                      value={member.role}
                      onChange={(e) => void changeRole(member.user_id, e.target.value as WorkspaceMemberRole)}
                      className="h-9 rounded-lg border border-line bg-card px-2 text-sm"
                    >
                      {roles.filter((r) => r !== "owner").map((role) => (
                        <option key={role} value={role}>{role}</option>
                      ))}
                    </select>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {inviteOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/50 p-4">
            <form onSubmit={invite} className="w-full max-w-md rounded-2xl border border-line bg-card p-5 shadow-panel">
              <h2 className="text-lg font-semibold text-foreground">Invite member</h2>
              <p className="mt-1 text-sm text-muted">Send an invitation by email with a workspace role.</p>
              <div className="mt-4 grid gap-3">
                <Input
                  type="email"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                  placeholder="colleague@university.edu"
                  required
                />
                <select
                  value={inviteRole}
                  onChange={(e) => setInviteRole(e.target.value as WorkspaceMemberRole)}
                  className="h-10 rounded-lg border border-line bg-panel px-3 text-sm"
                >
                  {roles.filter((r) => r !== "owner").map((role) => (
                    <option key={role} value={role}>{role}</option>
                  ))}
                </select>
              </div>
              <div className="mt-5 flex justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setInviteOpen(false)}>Cancel</Button>
                <Button type="submit" variant="primary" disabled={inviteLoading}>
                  <Mail className="h-4 w-4" />
                  Send invite
                </Button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}


