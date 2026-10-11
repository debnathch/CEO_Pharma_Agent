import {
  AgentManifest,
  ApprovalItem,
  DashboardSummary,
  EvaluationRun,
  ExecutionRecord,
  FeedbackRecord,
  ImprovementProposal,
  IntegrationHealth,
  MetricSummary,
} from "../types.ts";

const BASE_URL =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.PROD ? "/api/v1" : "http://localhost:8000/api/v1");

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${BASE_URL}/dashboard/summary`);
  if (!res.ok) throw new Error("Failed to load dashboard summary");
  return res.json();
}

export async function sendChatMessage(query: string) {
  const res = await fetch(`${BASE_URL}/ceo/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  return res.json();
}

export async function fetchDailyBriefing() {
  const res = await fetch(`${BASE_URL}/ceo/daily-briefing`);
  if (!res.ok) throw new Error("Failed to load daily briefing");
  return res.json();
}

export async function fetchAgents(): Promise<AgentManifest[]> {
  const res = await fetch(`${BASE_URL}/agents`);
  if (!res.ok) throw new Error("Failed to load agents");
  return res.json();
}

export async function fetchIntegrations(): Promise<IntegrationHealth[]> {
  const res = await fetch(`${BASE_URL}/integrations/status`);
  if (!res.ok) throw new Error("Failed to load integrations");
  return res.json();
}

export async function fetchExecutions(): Promise<ExecutionRecord[]> {
  const res = await fetch(`${BASE_URL}/executions?limit=50`);
  if (!res.ok) throw new Error("Failed to load executions");
  return res.json();
}

export async function fetchMetrics(): Promise<MetricSummary> {
  const res = await fetch(`${BASE_URL}/observability/metrics`);
  if (!res.ok) throw new Error("Failed to load metrics");
  return res.json();
}

export async function fetchEvaluations(): Promise<EvaluationRun[]> {
  const res = await fetch(`${BASE_URL}/evaluations`);
  if (!res.ok) throw new Error("Failed to load evaluations");
  return res.json();
}

export async function runEvaluationSuite(datasetVersion = "v1.0.0"): Promise<EvaluationRun> {
  const res = await fetch(`${BASE_URL}/evaluations/run?dataset_version=${datasetVersion}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to run evaluation suite");
  return res.json();
}

export async function fetchEvaluationRunDetail(runId: string): Promise<EvaluationRun> {
  const res = await fetch(`${BASE_URL}/evaluations/${runId}`);
  if (!res.ok) throw new Error("Failed to load evaluation run detail");
  return res.json();
}

export async function submitFeedback(
  executionId: string,
  rating: string,
  comment = ""
): Promise<FeedbackRecord> {
  const res = await fetch(`${BASE_URL}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      execution_id: executionId,
      rating,
      comment,
      reviewer_id: "executive-ui",
    }),
  });
  if (!res.ok) throw new Error("Failed to submit feedback");
  return res.json();
}

export async function fetchProposals(): Promise<{
  proposals: ImprovementProposal[];
  failure_analysis: any;
}> {
  const res = await fetch(`${BASE_URL}/improvement-proposals`);
  if (!res.ok) throw new Error("Failed to load improvement proposals");
  return res.json();
}

export async function reviewProposal(
  proposalId: string,
  decision: "approved" | "rejected",
  comments = ""
): Promise<ImprovementProposal> {
  const res = await fetch(`${BASE_URL}/improvement-proposals/${proposalId}/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      decision,
      reviewer_id: "Principal Architect",
      comments,
    }),
  });
  if (!res.ok) throw new Error("Failed to review proposal");
  return res.json();
}

export async function fetchApprovals(): Promise<ApprovalItem[]> {
  const res = await fetch(`${BASE_URL}/approvals`);
  if (!res.ok) throw new Error("Failed to load approvals");
  return res.json();
}

export async function actionApproval(approvalId: string, action = "approve") {
  const res = await fetch(`${BASE_URL}/approvals/${approvalId}/action?action=${action}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to action approval");
  return res.json();
}
