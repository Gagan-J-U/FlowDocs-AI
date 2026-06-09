import { Navigate, Route, Routes } from "react-router-dom";
import { ChatPanel } from "../components/ChatPanel";
import { ComparisonsPage } from "../pages/ComparisonsPage";
import { DocumentsPage } from "../pages/DocumentsPage";
import { MembersPage } from "../pages/MembersPage";
import { MessagesPage } from "../pages/MessagesPage";
import {
  DiscoverResearchersPage,
  ResearchDirectoryPage,
  ResearchProfilePage,
} from "../pages/ResearchPage";
import { SettingsPage } from "../pages/SettingsPage";
import { SubjectsPage } from "../pages/SubjectsPage";
import { WorkspaceChatPage } from "../pages/WorkspaceChatPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/chat" replace />} />
      <Route path="/chat" element={<ChatPanel />} />
      <Route path="/subjects" element={<SubjectsPage />} />
      <Route path="/documents" element={<DocumentsPage />} />
      <Route path="/comparisons" element={<ComparisonsPage />} />
      <Route path="/research" element={<ResearchDirectoryPage />} />
      <Route path="/research/discover" element={<DiscoverResearchersPage />} />
      <Route path="/research/profile/:userId" element={<ResearchProfilePage />} />
      <Route path="/members" element={<MembersPage />} />
      <Route path="/messages" element={<MessagesPage />} />
      <Route path="/workspace-chat" element={<WorkspaceChatPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="*" element={<Navigate to="/chat" replace />} />
    </Routes>
  );
}
