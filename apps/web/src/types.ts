export interface DashboardSummary {
  as_of_date: string;
  data_mode: string;
  ethical_sales: {
    total_achieved_mtd: number;
    total_target_mtd: number;
    overall_achievement_pct: number;
    top_performing_hq: string;
  };
  pcd_sales: {
    total_revenue: number;
    pending_orders: number;
    distributor_count: number;
  };
  billing: {
    total_invoiced_net: number;
    total_gross_profit: number;
    overall_gross_margin_pct: number;
    low_margin_alerts_count: number;
  };
  finance: {
    total_debtors_outstanding: number;
    critical_overdue_90d: number;
    critical_debtor_count: number;
  };
  procurement: {
    low_stock_skus_count: number;
    total_skus: number;
    alerts: string[];
  };
  logistics: {
    total_shipments: number;
    delayed_shipments_count: number;
    in_transit_count: number;
  };
  hr: {
    total_employees: number;
    birthdays_count: number;
    anniversaries_count: number;
  };
  provider_status: {
    provider_name: string;
    is_available: boolean;
    model_name: string;
    details: string;
    is_mock: boolean;
  };
}

export interface AgentCapability {
  name: string;
  description: string;
  input_schema_name: string;
  output_schema_name: string;
  is_implemented: boolean;
  requires_approval: boolean;
}

export interface AgentManifest {
  agent_id: string;
  display_name: string;
  description: string;
  domain: string;
  version: string;
  capabilities: AgentCapability[];
  implementation_status: "full" | "partial" | "skeleton";
  required_permissions: string[];
  supported_tools: string[];
  readiness_info: Record<string, any>;
}

export interface EvidenceReference {
  source_system: string;
  entity_type: string;
  entity_id: string;
  timestamp: string;
  authoritative: boolean;
  details: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "ceo";
  text: string;
  timestamp: string;
  agentsInvoked?: string[];
  evidence?: EvidenceReference[];
  warnings?: string[];
  durationMs?: number;
  providerUsed?: string;
  isMock?: boolean;
  executionId?: string;
}

export interface ExecutionRecord {
  id: number;
  execution_id: string;
  request_id: string;
  correlation_id: string;
  user_query: string;
  status: string;
  agents_invoked: string[];
  duration_ms: number;
  provider_mode: string;
  model_identifier: string;
  summary: string;
  evidence_count: number;
  warnings: string[];
  created_at: string;
  data_mode: string;
}

export interface IntegrationHealth {
  system_id: string;
  display_name: string;
  is_connected: boolean;
  is_mock: boolean;
  authority_scope: string;
  last_sync_timestamp: string;
  status_message: string;
}

export interface MetricSummary {
  total_requests: number;
  successful_executions: number;
  partial_executions: number;
  failed_executions: number;
  agent_invocation_counts: Record<string, number>;
  agent_success_rates: Record<string, number>;
  average_duration_ms: number;
  p95_duration_ms: number;
  provider_mode: string;
  provider_available: boolean;
}

export interface EvaluationResult {
  run_id: string;
  case_id: string;
  category: string;
  passed: boolean;
  failure_reason?: string;
  metric_results: any[];
  duration_ms: number;
}

export interface EvaluationRun {
  run_id: string;
  dataset_version: string;
  model_mode: string;
  model_identifier: string;
  total_cases: number;
  passed_cases: number;
  failed_cases: number;
  pass_rate: number;
  category_scores: Record<string, number>;
  regression_detected: boolean;
  created_at?: string;
  results?: EvaluationResult[];
}

export interface ImprovementProposal {
  proposal_id: string;
  title: string;
  description: string;
  target_agent_id: string;
  proposal_type: string;
  failure_category: string;
  rationale: string;
  proposed_changes: Record<string, any>;
  status: "draft" | "under_review" | "approved" | "rejected" | "released" | "rolled_back";
  reviewed_by?: string;
  review_comments?: string;
  regression_suite_passed: boolean;
  created_at: string;
}

export interface FeedbackRecord {
  feedback_id: string;
  execution_id: string;
  rating: string;
  comment?: string;
  reviewer_id: string;
  timestamp: string;
}

export interface ApprovalItem {
  id: string;
  type: string;
  title: string;
  requester: string;
  requested_at: string;
  estimated_cost: string;
  supplier: string;
  status: string;
  is_simulation: boolean;
  simulation_notice: string;
}
