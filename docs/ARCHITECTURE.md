# Enterprise Pharmaceutical Agentic AI Ecosystem — Architecture Specification

## 1. Executive Summary

This document specifies the software architecture for the **Enterprise Pharmaceutical Agentic AI Ecosystem** designed for **Bengal Remedies**. The platform provides an executive conversational interface for the Chief Executive Officer (CEO), bounded multi-agent orchestration, specialist agents across 10 functional domains, deterministic accounting services, mock enterprise integrations, zero-cost local LLM inference, structured observability, and an automated evaluation and continuous-improvement lifecycle.

---

## 2. System Context Diagram (C4 Level 1)

```mermaid
flowchart TD
    User["Executive User / CEO"] -->|Natural Language Inquiries| UI["React Command Center UI (Port 3000)"]
    UI -->|REST /api/v1| API["FastAPI Modular Monolith API (Port 8000)"]
    
    subgraph Enterprise_Ecosystem["Enterprise Pharmaceutical Multi-Agent Ecosystem"]
        API --> Orchestrator["CEO Master Orchestration Engine (LangGraph)"]
        Orchestrator --> Registry["Agent Registry & Contracts"]
        Registry --> Specialists["10 Specialist Agents"]
        Specialists --> BusinessServices["Deterministic Domain Services"]
        Specialists --> MockAdapters["Integration Adapters"]
        Orchestrator --> LLMProvider["LLM Provider Abstraction"]
        Orchestrator --> Observability["Observability Engine (Traces & Metrics)"]
        Orchestrator --> Persistence["Relational Persistence (SQLAlchemy)"]
        Orchestrator --> Evaluation["Evaluation & Regression Suite"]
    end

    subgraph External_Systems["External Business Systems (Mock Mode)"]
        MockAdapters -.-> MargERP["Marg ERP (Accounting Authority)"]
        MockAdapters -.-> Portal["B2B Ordering Portal (Order Workflow)"]
        MockAdapters -.-> WhatsApp["WhatsApp Field Feeds (Evidence Input)"]
    end

    subgraph Local_Inference["Local Machine Inference"]
        LLMProvider -->|HTTP :11434| Ollama["Ollama Daemon (qwen3:4b / llama3.2:3b)"]
        LLMProvider -->|Fallback| MockLLM["Mock LLM Provider (Deterministic)"]
    end
```

---

## 3. High-Level Layered Architecture (12 Logical Layers)

The platform is structured into 12 distinct logical layers within a modular monolith. Observability and evaluation are native first-class citizens, not peripheral utilities.

```mermaid
flowchart TB
    L1["Layer 1: User Interface & CEO Command Center (React, TypeScript, Vite)"]
    L2["Layer 2: API & Security Boundary (FastAPI /api/v1, CORS, Pydantic v2)"]
    L3["Layer 3: CEO Orchestration Engine (LangGraph Bounded StateGraph)"]
    L4["Layer 4: Agent Registry & Standardized Contracts (BaseAgent, AgentManifest)"]
    L5["Layer 5: Independent Specialist Agents (10 Domain Modules)"]
    L6["Layer 6: Shared Business Services (Deterministic Calculations)"]
    L7["Layer 7: Integration Adapters (Marg ERP, Portal, WhatsApp)"]
    L8["Layer 8: LLM Provider Abstraction (Ollama, Mock, Hosted Extension)"]
    L9["Layer 9: Persistence & Audit (SQLAlchemy, SQLite / PostgreSQL)"]
    L10["Layer 10: Observability & Telemetry (Correlation IDs, Spans, Metrics)"]
    L11["Layer 11: Agent Evaluation & Quality Measurement (EvaluationRunner, Datasets)"]
    L12["Layer 12: Continuous Improvement & Controlled Release (FailureAnalyzer, Review Gates)"]

    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> L6
    L5 --> L7
    L3 --> L8
    L3 --> L9
    L3 --> L10
    L9 --> L11
    L10 --> L11
    L11 --> L12
```

---

## 4. CEO Orchestration Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor CEO as Executive User
    participant UI as Command Center UI
    participant API as FastAPI Router
    participant WF as LangGraph Orchestrator
    participant Reg as Agent Registry
    participant Spec as Specialist Agent(s)
    participant Calc as Business Service
    participant LLM as LLM Provider (Ollama / Mock)
    participant Obs as Observability & DB

    CEO->>UI: Submit inquiry: "How is Kolkata HQ sales performing?"
    UI->>API: POST /api/v1/ceo/chat {query}
    API->>WF: run_ceo_workflow(query, context)
    WF->>Obs: Emit event: WORKFLOW_STARTED (trace_id)
    WF->>WF: classify_and_validate(intent)
    WF->>Reg: Discover agents for intent 'ethical_sales'
    Reg-->>WF: Return EthicalSalesAgent instance
    WF->>Spec: execute(AgentRequest)
    Spec->>Calc: SalesService.get_hq_sales_by_id_or_name("Kolkata")
    Calc-->>Spec: Return deterministic achievement (107.4%)
    Spec-->>WF: Return AgentResult (status=SUCCESS, structured_data, evidence)
    WF->>WF: aggregate_and_ground()
    WF->>LLM: generate(grounded_prompt)
    LLM-->>WF: Return executive summary
    WF->>Obs: Persist ExecutionRecord & emit FINAL_RESPONSE_RETURNED
    WF-->>API: Return WorkflowState
    API-->>UI: Return ChatResponse (JSON)
    UI-->>CEO: Render grounded response, agent pills, and evidence drawer
```

---

## 5. Agent Registration and Onboarding Architecture

New specialist agents are introduced without modifying the CEO Master Agent or existing agents.

```mermaid
flowchart LR
    Dev["Developer"] -->|1. Inherit| BaseAgent["BaseAgent (Abstract Base Class)"]
    Dev -->|2. Declare| Manifest["AgentManifest & Capabilities"]
    Dev -->|3. Register| Bootstrap["register_all_agents()"]
    Bootstrap --> Registry["AgentRegistry Singleton"]
    Registry -->|Enforce| UniqueCheck{"Duplicate Agent ID?"}
    UniqueCheck -->|Yes| Reject["Raise ValueError (Rejection)"]
    UniqueCheck -->|No| Store["Register in In-Memory Map"]
    Store --> Discovery["Available for CEO Dynamic Discovery"]
```

---

## 6. Integration Adapter Boundary & Data Ownership

```mermaid
flowchart TD
    subgraph Authority_Boundaries["Authoritative Business Ownership Boundaries"]
        Marg["Marg ERP Accounting Engine"] -->|Authority Over| MargScope["General Ledger, Invoices, COGS, Debtors, Creditors"]
        Portal["B2B Ordering Portal (Port 9000)"] -->|Authority Over| PortalScope["Order Submission, PCD Franchise Workflow"]
        WhatsAppFeed["WhatsApp Ingestion Stream"] -->|Non-Authoritative| WAEvidence["Unstructured Messages, Audio Notes (Evidence Only)"]
    end

    subgraph Platform_Adapters["Platform Mock Adapters"]
        MargAdapter["MargERPAdapter"] -.-> Marg
        PortalAdapter["OrderingPortalAdapter"] -.-> Portal
        WAAdapter["WhatsAppIngestionAdapter (Idempotent Deduplication)"] -.-> WhatsAppFeed
    end

    Platform_Adapters --> Specialists["Specialist Agents (ethical_sales, billing, finance, pcd_sales)"]
```

---

## 7. Observability Event and Trace Flow

```mermaid
flowchart TD
    Req["Incoming Request (request_id, correlation_id)"] --> StartSpan["Start TraceSpan (TraceContext)"]
    StartSpan --> Ev1["Event: WORKFLOW_STARTED"]
    Ev1 --> Ev2["Event: AGENT_SELECTED (ethical_sales)"]
    Ev2 --> Ev3["Event: AGENT_EXECUTION_COMPLETED"]
    Ev3 --> Ev4["Event: PROVIDER_CALL_COMPLETED (duration_ms)"]
    Ev4 --> Ev5["Event: FINAL_RESPONSE_RETURNED"]
    
    Ev1 & Ev2 & Ev3 & Ev4 & Ev5 --> JSONLog["Structured JSON Logger (Stdout)"]
    Ev1 & Ev2 & Ev3 & Ev4 & Ev5 --> MetricsCollector["MetricsCollector (In-Memory Telemetry)"]
    Ev5 --> DBPersistence["ExecutionRecordModel (SQLite / Postgres)"]
    
    MetricsCollector --> MetricsAPI["GET /api/v1/observability/metrics"]
    DBPersistence --> HistoryAPI["GET /api/v1/executions"]
```

---

## 8. Agent Evaluation Pipeline

```mermaid
flowchart TD
    Dataset["Evaluation Dataset v1.0.0 (12 Cases across 9 Categories)"] --> Runner["EvaluationRunner"]
    Runner --> ExecHarness["run_ceo_workflow() against Active Provider"]
    ExecHarness --> Evaluator["DeterministicEvaluator"]
    
    subgraph Checks["Deterministic Verification Checks"]
        Evaluator --> CheckRouting["1. Routing Accuracy"]
        Evaluator --> CheckContract["2. Contract Conformance"]
        Evaluator --> CheckData["3. Business Data Correctness"]
        Evaluator --> CheckEvidence["4. Evidence Linkage"]
        Evaluator --> CheckSafety["5. Safety & Policy Compliance"]
        Evaluator --> CheckRobustness["6. Robustness & Error Handling"]
    end

    Checks --> Result["EvaluationRunSummary (Pass Rate, Category Scores)"]
    Result --> CompareBaseline{"Pass Rate >= 90% Baseline?"}
    CompareBaseline -->|Yes| Stable["Flag Stable Baseline (Zero Regression)"]
    CompareBaseline -->|No| Alert["Flag REGRESSION_DETECTED"]
    Stable & Alert --> SaveRun["Persist EvaluationRunModel"]
```

---

## 9. Continuous Improvement Lifecycle (Controlled Governance)

```mermaid
flowchart TD
    ProdExec["Execution Captured (ExecutionRecord)"] --> Feedback["Reviewer Feedback (helpful, incorrect, unsupported)"]
    Feedback --> Analyzer["FailureAnalyzer (Root Cause Diagnosis)"]
    Analyzer --> ProposalEngine["ProposalEngine (Create ImprovementProposal)"]
    ProposalEngine --> ReviewQueue{"Human Review Gate (Architect / Reviewer)"}
    
    ReviewQueue -->|Reject| Rejected["Mark Proposal REJECTED"]
    ReviewQueue -->|Approve| Approved["Mark Proposal APPROVED"]
    
    Approved --> RegressionTest["Run EvaluationRunner (Regression Suite)"]
    RegressionTest --> TestPass{"All Baseline Cases Passed?"}
    TestPass -->|No| Rollback["Block Release (Candidate Regression)"]
    TestPass -->|Yes| Released["Mark Proposal RELEASED (Controlled Release)"]
```

---

## 10. Deployment Architecture (Local & Docker)

```mermaid
flowchart TD
    subgraph Host["Developer Workstation / Server"]
        subgraph Docker_Compose["Docker Compose / Native System"]
            WebContainer["Frontend Container (Nginx / Vite) :3000"]
            APIContainer["FastAPI Backend (Uvicorn / Python 3.12) :8000"]
            DBContainer["PostgreSQL Container (or Local SQLite) :5432"]
        end
        
        subgraph Native_Daemon["Local Inference Host"]
            OllamaHost["Ollama Service (:11434)\nModels: qwen3:4b, llama3.2:3b"]
        end
    end

    Browser["User Web Browser"] -->|HTTP :3000| WebContainer
    WebContainer -->|Proxy /api| APIContainer
    APIContainer -->|SQLAlchemy| DBContainer
    APIContainer -->|HTTP Localhost| OllamaHost
```

---

## 11. Data Ownership and Persistence Boundaries

| Entity | Primary Authority | Persistence Model | Storage Location | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Invoices & COGS | Marg ERP | Synthetic Fixture | Memory / ERP Ledger | Deterministic calculation source |
| Debtors & Aging | Marg ERP | Synthetic Fixture | Memory / AR Register | Exact 0-30, 31-60, 61-90, >90 day buckets |
| Franchise Orders | B2B Ordering Portal | Synthetic Fixture | Memory / Portal DB | PCD order intake authority |
| WhatsApp Messages | Field Groups | Synthetic Ingest | Memory Fixture | Evidence only; non-authoritative |
| Execution Records | AI Platform | `ExecutionRecordModel` | SQLite / PostgreSQL | Persisted telemetry with correlation IDs |
| Feedback Records | Reviewer Workflow | `FeedbackRecordModel` | SQLite / PostgreSQL | Human-in-the-loop audit |
| Evaluation Runs | Quality Harness | `EvaluationRunModel` | SQLite / PostgreSQL | Versioned test run results |
| Improvement Proposals | Release Governance| `ImprovementProposalModel`| SQLite / PostgreSQL | Human-reviewed improvement items |
