# Enterprise Pharmaceutical Agentic AI Ecosystem

> **Bengal Remedies** • CEO Master Intelligence Agent • Extensible Multi-Agent Platform • Zero-Cost Local LLM Inference • Full Observability & Continuous Improvement

---

## 1. Executive Summary

This repository contains the foundation-phase implementation of the **Enterprise Pharmaceutical Agentic AI Ecosystem** for **Bengal Remedies**. It provides an executive conversational interface for the Chief Executive Officer (CEO), bounded multi-agent orchestration via LangGraph, specialist agents across 10 functional domains, deterministic accounting services, mock external integration adapters, zero-cost local LLM inference via Ollama (with offline mock fallback), structured observability, an automated evaluation suite, and a controlled continuous-improvement governance lifecycle.

Built as a clean **Modular Monolith** in Python 3.12 / FastAPI with a React / TypeScript / Vite command center, this framework demonstrates senior software architecture, AI platform engineering, and enterprise governance principles suitable for a Google-level technical review.

---

## 2. Key Architectural Decisions (ADR Summary)

- **Modular Monolith over Microservices ([ADR-001](docs/DECISIONS/ADR-001-modular-monolith.md))**: In-process typed contracts eliminate premature network serialization tax, distributed transaction complexity, and Docker-mandated local dev overhead. Full test suite executes in **0.4 seconds**.
- **Bounded LangGraph StateGraph ([ADR-002](docs/DECISIONS/ADR-002-langgraph-bounded-workflow.md))**: Replaced unpredictable autonomous ReAct loops with a bounded, typed state machine: `classify_and_validate -> execute_specialists -> aggregate_and_ground -> synthesize -> record`.
- **Free Local LLM Strategy ([ADR-003](docs/DECISIONS/ADR-003-local-ollama-vs-hosted-llm.md) & [ADR-004](docs/DECISIONS/ADR-004-mock-provider-offline-fallback.md))**: Zero paid commercial API fees. Connects to local Ollama (`qwen3:4b`, `llama3.2:3b`) with a fully offline, deterministic `MockLLMProvider` fallback for automated CI and instant local development.
- **Deterministic Math Separated from Probabilistic LLM ([ADR-005](docs/DECISIONS/ADR-005-deterministic-calculations.md))**: Financial accounting, gross margin %, debtor aging, and inventory deficit calculations run in audited Python services. The LLM strictly narrates verified facts.
- **Relational Storage ([ADR-006](docs/DECISIONS/ADR-006-persistence-storage.md))**: PostgreSQL-ready schema with zero-dependency SQLite local development.
- **No Premature Vector Databases ([ADR-007](docs/DECISIONS/ADR-007-memory-deferred.md))**: Structured ledgers and catalogs are queried relationally. Semantic memory is deferred to Phase 5.
- **Vendor-Neutral Observability ([ADR-008](docs/DECISIONS/ADR-008-observability-design.md))**: Unified correlation IDs, structured JSON logs, trace spans, and p95 latency telemetry.
- **Objective Evaluation Framework ([ADR-009](docs/DECISIONS/ADR-009-evaluation-methodology.md))**: Deterministic verification suite covering 12 test cases across 9 categories with automated regression gating.
- **Controlled Continuous Improvement ([ADR-010](docs/DECISIONS/ADR-010-continuous-improvement.md))**: Agents **never** autonomously rewrite production code. Improvements require structured diagnosis, proposals, human review, and regression verification.

---

## 3. Specialist Agent Catalog

All 10 agents inherit from `BaseAgent`, declare a static `AgentManifest`, and report truthful readiness:

| Agent ID | Display Name | Domain | Readiness | Capabilities Implemented |
| :--- | :--- | :--- | :--- | :--- |
| `ceo_master` | CEO Master Intelligence | Executive Leadership | **FULL** | Intent classification, dynamic routing, briefing synthesis |
| `ethical_sales` | Ethical Sales Agent | Ethical Sales | **PARTIAL** | MTD HQ targets, achievements, top reps, HQ detail |
| `pcd_sales` | PCD Franchise Sales | PCD Distribution | **PARTIAL** | Consolidated franchise revenue, distributor standings |
| `procurement` | Procurement & Inventory | Supply Chain | **PARTIAL** | Stock levels, reorder threshold alerts, suggested units |
| `billing` | Billing & Commercial | Commercial | **PARTIAL** | Net sales, COGS, free goods costs, gross margin % |
| `finance` | Finance & Accounts | Accounts Receivable | **PARTIAL** | Debtor aging buckets (0-30, 31-60, 61-90, >90d), creditors |
| `logistics` | Logistics & Tracking | Supply Chain | **PARTIAL** | Active consignments, LR tracking, delay detection |
| `marketing` | Digital Marketing Agent | Brand & Content | **PARTIAL** | Campaign draft staging (External publishing disabled) |
| `product_launch`| Product Launch & LBL | Medical Affairs | **PARTIAL** | Pipeline launches, LBL doctor brochures with disclaimers |
| `hr` | Human Resources Agent | Human Resources | **PARTIAL** | Employee birthdays, work anniversaries, payslip staging |

*Note*: Unimplemented capabilities (such as unapproved purchase order submissions or live social media publishing) return honest `AgentStatus.NOT_IMPLEMENTED` rather than hallucinated execution.

---

## 4. Repository Structure

```text
├── apps/
│   ├── api/                     # FastAPI backend application
│   │   ├── main.py              # Application entrypoint & lifespan
│   │   └── routes.py            # Versioned API routes (/api/v1/*)
│   └── web/                     # React + TypeScript + Vite frontend
│       ├── src/
│       │   ├── pages/           # 9 executive dashboard views
│       │   ├── services/api.ts  # API client
│       │   ├── App.tsx          # Navigation shell & status badges
│       │   └── index.css        # Executive dark theme
├── src/
│   └── pharma_platform/
│       ├── agents/              # 10 specialist agent modules
│       ├── business_services/   # Deterministic domain calculations
│       ├── configuration/       # Centralized Pydantic settings
│       ├── contracts/           # Pydantic schemas (Agent, Tool, Eval)
│       ├── data/synthetic/      # Realistic pharmaceutical fixtures
│       ├── evaluation/          # Evaluation runner & v1.0.0 datasets
│       ├── improvement/         # Feedback & proposal review engine
│       ├── integrations/        # Mock adapters (Marg, Portal, WhatsApp)
│       ├── observability/       # Logger, tracer & metrics collector
│       ├── orchestration/       # LangGraph bounded StateGraph workflow
│       ├── persistence/         # SQLAlchemy models & database engine
│       ├── providers/           # LLM providers (Mock, Ollama, Hosted)
│       └── registry/            # Agent registry & BaseAgent class
├── tests/
│   ├── unit/                    # Business services, registry, providers
│   ├── contract/                # Agent manifests & schemas
│   ├── integration/             # FastAPI endpoints & multi-agent chat
│   └── evaluation/              # Baseline regression suite
├── docs/                        # Comprehensive architecture documentation
│   ├── ARCHITECTURE.md          # 10 Mermaid diagrams & 12 logical layers
│   ├── AGENT_CATALOG.md         # Full specialist agent directory
│   ├── AGENT_DEVELOPMENT_GUIDE.md # 10-step agent onboarding walkthrough
│   ├── ORCHESTRATION.md         # LangGraph bounded state machine
│   ├── LLM_CONFIGURATION.md     # Free local Ollama setup & models
│   ├── DATA_MODEL.md            # Relational models & ownership rules
│   ├── INTEGRATIONS.md          # Mock integration adapters
│   ├── SECURITY.md              # Security, write-isolation & privacy
│   ├── OBSERVABILITY.md         # Tracing, events & telemetry metrics
│   ├── EVALUATION.md            # 9 evaluation categories & datasets
│   ├── CONTINUOUS_IMPROVEMENT.md # Controlled release & review gates
│   ├── ROADMAP.md               # Phase 1 to Phase 5 platform roadmap
│   ├── INTERVIEW_WALKTHROUGH.md # Senior technical interview narrative
│   └── DECISIONS/               # 11 Architecture Decision Records (ADRs)
├── pyproject.toml               # Python project configuration
├── Dockerfile                   # Multi-stage production Dockerfile
└── docker-compose.yml           # API + PostgreSQL container composition
```

---

## 5. Quickstart & Native Local Execution

### Prerequisites
- Python 3.12+ (managed via `uv` or native)
- Node.js 18+ and npm
- (Optional) Ollama for local model inference

### Step 1: Clone and Setup Virtual Environment
```bash
# Create virtual environment and install dependencies
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Step 2: Run Backend Tests & Linting
```bash
# Execute full test suite (27 passed in 0.4s)
pytest tests/

# Execute linter checks
ruff check .
```

### Step 3: Start the Backend API Server
```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
```
API docs available at: `http://localhost:8000/docs`

### Step 4: Start the React Frontend Command Center
In a separate terminal:
```bash
cd apps/web
npm install
npm run dev
```
Open your browser at: `http://localhost:3000`

---

## 6. Local Free LLM Setup (Ollama)

By default, the platform boots in `LLM_PROVIDER=mock` mode for instant offline execution.

To enable local model inference:
1. Install Ollama:
   ```bash
   # macOS
   brew install ollama
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Start the daemon and download the candidate model:
   ```bash
   ollama serve
   ollama pull qwen3:4b
   ```
3. Update `.env`:
   ```bash
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=qwen3:4b
   ```
4. Restart the API server. The UI badge updates to reflect the active provider.

---

## 7. Example CEO Inquiries via cURL

### 1. Ethical Sales Performance
```bash
curl -X POST "http://localhost:8000/api/v1/ceo/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "How is Kolkata HQ sales performing this month?"}'
```

### 2. Critical Stock Deficit & Reorder Alerts
```bash
curl -X POST "http://localhost:8000/api/v1/ceo/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which pharmaceutical stocks are below safety reorder threshold?"}'
```

### 3. Accounts Receivable Overdue Debtors
```bash
curl -X POST "http://localhost:8000/api/v1/ceo/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me overdue debtors and accounts receivable aging"}'
```

### 4. Consolidated Daily Morning Briefing
```bash
curl -X GET "http://localhost:8000/api/v1/ceo/daily-briefing"
```

### 5. Execute Evaluation Suite
```bash
curl -X POST "http://localhost:8000/api/v1/evaluations/run?dataset_version=v1.0.0"
```

---

## 8. Verification & Test Outcomes

- **Unit Tests**: Deterministic sales achievement %, gross profit margins, debtor aging buckets, inventory reorder math, provider abstraction error handling.
- **Contract Tests**: All 10 agents conform to `AgentManifest` schemas; truthful `not_implemented` statuses verified.
- **Integration Tests**: FastAPI endpoints, CEO chat routing, evidence aggregation, execution persistence, feedback submission, proposal listing.
- **Evaluation Suite**: 12/12 cases passed (100% pass rate) across routing accuracy, contract validity, data correctness, evidence coverage, groundedness, task completion, safety & policy, and robustness.
- **Frontend Production Build**: `tsc && vite build` completed in 648ms with 0 errors.

---

## 9. License & Author

Developed for **Bengal Remedies** as an extensible foundation architecture for enterprise agentic AI.
All data in this foundation release is purely synthetic.
