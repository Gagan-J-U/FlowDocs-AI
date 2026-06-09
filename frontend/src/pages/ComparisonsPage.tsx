import { ComparisonPanel } from "../components/ComparisonPanel";
import { EmptyState } from "../components/ui/empty-state";
import { GitCompareArrows } from "lucide-react";
import { useAppStore } from "../store/app-store";

export function ComparisonsPage() {
  const { selectedSubjectId } = useAppStore();

  if (!selectedSubjectId) {
    return (
      <EmptyState
        icon={GitCompareArrows}
        title="Select a subject"
        description="Pick a subject with at least two documents to run comparisons."
      />
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto p-6">
      <div className="mx-auto max-w-5xl">
        <ComparisonPanel />
      </div>
    </div>
  );
}
