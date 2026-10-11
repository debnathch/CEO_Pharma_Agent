# Data Model & Persistence Boundaries

## 1. Data Ownership Architecture

In an enterprise pharmaceutical business, system-of-record ownership must be explicit:
- **Marg ERP** owns general ledger, accounting entries, product costing, invoices, and debtor/creditor balances.
- **B2B Ordering Portal** (`http://bengalremedies.com:9000`) owns order workflows, franchise order submissions, and pending dispatch queues.
- **WhatsApp Feeds** are an input source of unstructured evidence and field notes; they are **never** authoritative accounting records without reconciliation.
- **AI Platform Database** persists platform execution traces, telemetry, evaluation benchmarks, feedback records, and improvement proposals.

---

## 2. Platform Relational Schema (SQLAlchemy ORM)

### `execution_records`
Stores complete telemetry for every CEO orchestrator run.
- `id` (PK, Integer)
- `request_id` (String 64, Indexed)
- `execution_id` (String 64, Unique, Indexed)
- `correlation_id` (String 64, Indexed)
- `user_query` (Text)
- `workflow_status` (String 32: `success`, `partial`, `failed`)
- `agents_invoked` (JSON: Array of agent IDs)
- `duration_ms` (Float)
- `provider_mode` (String 32: `mock`, `ollama`)
- `model_identifier` (String 64)
- `structured_data` (JSON: Merged specialist agent payloads)
- `summary` (Text: Synthesized natural language response)
- `evidence_count` (Integer)
- `warnings` (JSON: Array of domain warnings)
- `error_category` (String 64, Nullable)
- `data_mode` (String 32: `synthetic`)
- `created_at` (DateTime, Indexed)

### `feedback_records`
Stores human review labels attached to specific executions.
- `id` (PK, Integer)
- `feedback_id` (String 64, Unique)
- `execution_id` (String 64, Indexed)
- `rating` (String 32: `helpful`, `incorrect`, `incomplete`, `unsupported`)
- `comment` (Text)
- `reviewer_id` (String 64)
- `created_at` (DateTime)

### `evaluation_runs`
Stores benchmark outcomes from the automated evaluation suite.
- `id` (PK, Integer)
- `run_id` (String 64, Unique)
- `dataset_version` (String 32, e.g. `v1.0.0`)
- `model_mode` (String 32)
- `model_identifier` (String 64)
- `total_cases` (Integer)
- `passed_cases` (Integer)
- `failed_cases` (Integer)
- `pass_rate` (Float: 0.0 - 1.0)
- `category_scores` (JSON: Map of category scores)
- `results_json` (JSON: Array of per-case outcomes)
- `regression_detected` (Boolean)
- `created_at` (DateTime)

### `improvement_proposals`
Stores proposed prompt, routing, or policy improvements for human review.
- `id` (PK, Integer)
- `proposal_id` (String 64, Unique)
- `title` (String 256)
- `description` (Text)
- `target_agent_id` (String 64)
- `proposal_type` (String 64: `prompt_refinement`, `routing_keyword_update`, etc.)
- `failure_category` (String 64)
- `rationale` (Text)
- `proposed_changes` (JSON)
- `status` (String 32: `draft`, `under_review`, `approved`, `rejected`, `released`)
- `reviewed_by` (String 64, Nullable)
- `review_comments` (Text, Nullable)
- `regression_suite_passed` (Boolean)
- `created_at` (DateTime)

### `audit_events`
Audit log recording policy-relevant actions.
- `id` (PK, Integer)
- `event_id` (String 64, Unique)
- `action` (String 64)
- `user_id` (String 64)
- `details` (JSON)
- `created_at` (DateTime)
