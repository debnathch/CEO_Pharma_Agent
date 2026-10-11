# Enterprise Technical Interview Walkthrough

## Google-Level Principal Architect & Staff AI Engineer Presentation Narrative

---

## 1. Executive Problem Definition

Bengal Remedies is an established pharmaceutical manufacturing and distribution business operating across ethical sales (HQ-based), PCD franchise networks, procurement, factory operations, commercial billing, finance, logistics, and HR.

The executive leadership team faces severe data fragmentation:
- **Marg ERP** holds transactional ledgers and invoices.
- A **B2B Ordering Portal** (`bengalremedies.com:9000`) manages franchise order streams.
- **WhatsApp groups** contain informal field updates, driver delay notices, and urgent doctor requests.

The goal was to design and construct a production-ready, extensible multi-agent AI ecosystem that empowers the CEO with grounded conversational intelligence, unifies cross-departmental evidence, enforces deterministic business math, runs on free local LLMs, and embeds enterprise-grade observability, evaluation, and controlled continuous improvement from Day 1.

---

## 2. Core Architectural Philosophy & Trade-Offs

### A. Modular Monolith vs. Microservices (ADR-001)
- **Trade-off**: Many engineers reflexively propose 10 independent microservices communicating via Kafka or gRPC.
- **Senior Technical Decision**: We deliberately rejected microservices in this phase. Premature distribution introduces network serialization overhead, eventual consistency hazards, complex distributed tracing, and local development friction. Instead, we implemented a **Modular Monolith** in Python 3.12 / FastAPI with strict package isolation (`src/pharma_platform/*`). Inter-agent calls occur in-process using typed Pydantic contracts. This achieves 0.4s test execution and effortless local developer onboarding, while keeping clean boundaries that can be split into services if traffic justifies it later.

### B. Bounded LangGraph Workflow vs. Autonomous ReAct Planner (ADR-002)
- **Trade-off**: Autonomous ReAct agents (looping between thought, action, observation) look impressive in toy demos but are notoriously fragile in enterprise settings—suffering from infinite loops, unpredictable latency, hallucinated sub-goals, and policy violations.
- **Senior Technical Decision**: We modeled the CEO Master Agent as an explicit, bounded state graph using **LangGraph**:
  `classify_and_validate -> execute_specialists -> aggregate_and_ground -> synthesize_executive_response -> record_and_evaluate`.
  This guarantees bounded execution time, typed state propagation, and step-by-step observability.

### C. Separation of Deterministic Math from Probabilistic LLM Reasoning (ADR-005)
- **Senior Technical Decision**: LLMs are statistical token predictors, not calculators. All gross profit calculations (`Gross Profit = Net Sales - [COGS + Scheme Cost]`), aging day buckets, and inventory deficit thresholds are executed in tested Python business services. The LLM's role is strictly confined to executive narration and contextual synthesis over verified numbers.

---

## 3. Free Local LLM Strategy & Observability

- **Zero-Cost Inference**: The platform avoids commercial per-token API costs by interfacing with local **Ollama** daemons (`http://localhost:11434`) running `qwen3:4b` or `llama3.2:3b`.
- **Mock Fallback**: A deterministic `MockLLMProvider` is always available.
- **Honest Error Handling**: If Ollama crashes or times out, the system never fabricates success; it returns an honest error message and falls back to a deterministic synthesis of the verified agent evidence.
- **Observability**: Every request receives a `correlation_id` and `execution_id`. The platform emits structured JSON logs, maintains OpenTelemetry-compatible trace spans, and records p95 latency and agent success rates.

---

## 4. Evaluation & Continuous Improvement Frameworks

- **No Self-Judging LLM Anti-Pattern**: We rejected "LLM-as-a-judge" for core evaluation. Our `EvaluationRunner` executes synthetic dataset `v1.0.0` (12 cases across 9 categories) and evaluates schema validity, routing accuracy, deterministic arithmetic, and absence of prohibited claims using deterministic assertions.
- **Controlled Continuous Improvement**: Agents **never** autonomously rewrite code or deploy unreviewed prompts. Reviewers label executions via `POST /api/v1/feedback`. The `FailureAnalyzer` diagnoses recurring failure modes, the `ProposalEngine` generates structured proposals, human reviewers approve or reject, and the regression suite must pass before any candidate prompt or routing change is released.

---

## 5. Ten Likely Architecture Interview Questions & Senior Answers

### Q1: Why didn't you use a vector database (RAG) for the business data?
> **Answer**: Financial ledgers, sales targets, invoice line items, and stock quantities are structured relational data. Querying financial statements via vector cosine similarity is an architectural anti-pattern that leads to hallucinated accounting values. Vector databases are appropriate for unstructured text (medical journals, SOPs), which we have scheduled for Phase 5. For structured enterprise data, relational databases and deterministic business services are the authoritative solution.

### Q2: How does adding an 11th specialist agent work without modifying the CEO agent?
> **Answer**: All agents inherit from `BaseAgent` and declare an `AgentManifest` listing their capabilities and domain. The CEO orchestrator discovers agents dynamically at runtime via `AgentRegistry.find_by_capability()`. Adding an agent requires only implementing the contract and registering it in bootstrap; no conditional branches in the CEO workflow need modification.

### Q3: What happens if Ollama local inference times out or runs out of VRAM?
> **Answer**: `OllamaLLMProvider` has a configurable timeout (default 30s) and catches `httpx.ConnectError` and timeout exceptions cleanly. Instead of failing the user request, it returns an explicit error string. The CEO orchestrator detects this and activates its deterministic fallback, generating an executive bullet-point summary directly from the verified specialist agent outputs and appending a provider warning to the UI.

### Q4: How do you prevent prompt injection from untrusted WhatsApp messages?
> **Answer**: External WhatsApp content is imported into isolated data payloads by the `WhatsAppIngestionAdapter`. In the orchestrator prompt, untrusted message text is strictly cordoned inside an evidence data container, separate from the system instructions and user query. Furthermore, the foundation phase enforces zero-write isolation, meaning no natural language prompt—injected or otherwise—can execute purchase orders or financial disbursements.

### Q5: How do you ensure idempotent processing of duplicate WhatsApp messages?
> **Answer**: Field representatives frequently resend order messages. The `WhatsAppIngestionAdapter` implements message deduplication by generating a content hash of `sender + text` and filtering duplicates during ingestion, ensuring non-authoritative messages do not distort evidence counters.

### Q6: Why did you choose LangGraph over autonomous multi-agent frameworks like AutoGen or CrewAI?
> **Answer**: AutoGen and CrewAI prioritize emergent conversational autonomy, which is unpredictable and prone to infinite loops and non-deterministic agent chatter. In enterprise pharmaceutical systems, predictability, latency guarantees, and auditability are paramount. LangGraph provides an explicit directed state graph where every state transition is typed, bounded, and traceable.

### Q7: How are gross profit and free-goods margin leakage calculated?
> **Answer**: In `BillingService`, gross profit is computed deterministically as:
> `Gross Profit = Net Sales Amount - (Cost of Goods Sold + Free Goods / Scheme Cost)`.
> `Gross Margin % = (Gross Profit / Net Sales Amount) * 100`.
> Invoices where margin falls below 15% due to excessive promotional bonus goods (e.g. `INV-2026-4409` at 9.09%) are flagged with low-margin warnings.

### Q8: What is your database migration and storage strategy?
> **Answer**: We use SQLAlchemy 2.x declarative models and Alembic. For local development and testing, SQLite (`sqlite:///./data/pharma.db`) provides zero-dependency execution. For production, setting `DATABASE_URL` targets PostgreSQL (`postgresql+psycopg://...`) without altering application code or ORM queries.

### Q9: How do you prevent regressions when an agent prompt or routing rule is updated?
> **Answer**: Before any `ImprovementProposal` can transition to `released`, it must run against the `EvaluationRunner` regression suite. If the overall pass rate drops below the 90% baseline or any deterministic test case fails, the release is blocked and flagged with `REGRESSION_DETECTED`.

### Q10: What are the current known limitations of the foundation phase?
> **Answer**:
> 1. Specialist agents return truthful `not_implemented` statuses for complex future capabilities (e.g. doctor call report OCR, unapproved payment runs).
> 2. External integrations are mock adapters rather than live ERP connections.
> 3. Small local quantized models (3B-4B) require explicit prompt grounding compared to 70B+ cloud models.
> 4. Semantic vector search across PDF documents is deferred to Phase 5.
